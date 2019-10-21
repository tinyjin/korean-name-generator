import trained_data as trainedData
import random
import math


def generateCustom(trainedDataMatrix):
    """
    랜덤한 한국 이름을 생성한다.

    :arg isMale: 남자 또는 여자의 성별 여부.
    """

    def ensure(n):
        return n or 0

    # 요소들의 가중치에 비례한 확률로 랜덤 뽑기
    def pick(count, item):
        sum = 0
        selected = 0

        for i in range(count):
            sum += item(i)

        pivot = random.random() * sum

        for i in range(count):
            pivot -= item(i)
            if pivot <= 0:
                selected = i
                break

        return selected

    # 랜덤으로 음절 생성
    def pickSyllable(set):
        try:
            choseong = pick(19, lambda n: ensure(trainedDataMatrix[set][0][n]))
        except Exception:
            choseong = 0

        try:
            jungseong = pick(21, lambda n: ensure(trainedDataMatrix[set][1][choseong * 21 + n]))
        except Exception:
            jungseong = 0

        try:
            jongseong = pick(28, lambda n: ensure(trainedDataMatrix[set][2][jungseong * 28 + n]) * ensure(trainedDataMatrix[set][3][choseong * 28 + n]))
        except Exception:
            jongseong = 0

        return constructFromJamoIndex([choseong, jungseong, jongseong])

    def pickLastName():
        lastNameIndex = pick(len(trainedData.lastNames), lambda n: trainedData.lastNameFrequency[n])

        return chr(trainedData.lastNames[lastNameIndex] + 0xAC00)

    return pickLastName() + pickSyllable(0) + pickSyllable(1)


def generate(isMale=True):
    return generateCustom(trainedData.firstNames[0 if isMale else 1])


def train(nameList, compress=False):
    """
    이름 리스트를 토대로 통계적 학습 데이터를 생성한다.

    :arg nameList: 학습할 이름 목록
    """

    trainedNameData = [[[], [], [], []], [[], [], [], []]]

    def increase(array, index):
        array[index] = (array[index] + 1 if array[index] else 1)
    

    def process(set, jamo):
        increase(trainedNameData[set][0], jamo[0])
        increase(trainedNameData[set][1], jamo[0] * 21 + jamo[1])
        increase(trainedNameData[set][2], jamo[1] * 28 + jamo[2])
        increase(trainedNameData[set][3], jamo[0] * 28 + jamo[2])

    for i in range(len(nameList)):
        firstName = nameList[i].substring(1)

        cheot = firstName.charAt(0)
        du = firstName.charAt(1) if len(firstName) > 0 else ''

        cheotJamo = resolveToJamoIndex(cheot)
        duJamo = resolveToJamoIndex(du)

        if cheotJamo: process(0, cheotJamo)
        if duJamo: process(1, duJamo)

    return compressEmptyPart(trainedNameData) if compress else trainedNameData


def compressEmptyPart(array):
    """
    빈 공간이 많은 배열을 압축한다.

    :param array: 압축할 대상 배열
    """

    compressedArray = []
    emptyCount = 0

    for i in range(len(array)):

        if not array[i]:
            emptyCount += 1
        elif type(array[i]) == list:
            compressedArray.append(compressEmptyPart(array[i]))

        else:
            if emptyCount > 0:
                compressedArray.append(-emptyCount)
                emptyCount = 0
                
            compressedArray.append(array[i])

    return compressedArray


def uncompressEmptyPart(array):
    """
    압축된 배열을 원래 상태로 되돌린다.

    :arg array: 압축 해제할 대상 배열
    """
    originalArray = []

    for i in range(len(array)):

        if type(array[i]) == list:
            originalArray.append(uncompressEmptyPart(array[i]))

        else:

            if array[i] >= 0:
                originalArray.append(array[i])
            else:
                for j in range(-array[i]):
                    originalArray.append(0)

    return originalArray


def constructFromJamoIndex(jamoIndex):
    """
    자모 배열로부터 음절을 생성한다.

    :param jamoIndex:
    """
    return chr(0xAC00 + 28 * 21 * jamoIndex[0] + 28 * jamoIndex[1] + jamoIndex[2])


def resolveToJamoIndex(syllable):
    """
    음절로부터 자보 배열을 생성한다.

    :param syllable:
    """

    code = syllable.charCodeAt(0) - 0xAC00

    choseong = math.floor(((code - code % 28) / 28) / 21)
    jungseong = math.floor(((code - code % 28) / 28) % 21)
    jongseong = code % 28

    def isValid(n):
        return n >= 0 if not n.isdigit() else False

    if not (isValid(choseong) and isValid(jungseong) and isValid(jongseong)):
        return None

    return [choseong, jungseong, jongseong]

trainedData.firstNames = uncompressEmptyPart(trainedData.firstNames)


if __name__ == '__main__':
    maleName = generate(True)
    print(maleName)
