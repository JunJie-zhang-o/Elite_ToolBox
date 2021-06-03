from merry import Merry

from inc.Class_merry import MyMerry


# @MyMerry.merry._try
def process(num1, num2, file):
    result = num1 / num2
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(result))

@MyMerry.merry._try
def text(num1, num2, file):
    process(num1, num2, file)


if __name__ == '__main__':
    # process(1, 2, 'result/result.txt')
    # process(1, 0, 'result.txt')
    # process(1, 2, 'result.txt')
    # process(1, [1], 'result.txt')
    
    text(1, 2, 'result/result.txt')