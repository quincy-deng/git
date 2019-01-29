#命名、统计、字典
##元组使用，节约内存，访问快
  # student = ('Jim',16,'male','jim@gamil.com')
NAME,AGE,SEX,EMAIL=range(4)
from collections import namedtuple
Student = namedtuple('Student',['name','age','sex','email'])
s =Student('Jim',16,'male','jim@gamil.com')
  #print(s.name)
#统计词频
from random import randint
a = [randint(0,20)for _ in range(30)]
from collections import Counter
c2 = Counter(a)
from random import randint
dic = {x: randint(60,90) for x in 'qhdurocl'}
dic2 = sorted(dic.items(),key=lambda x: x[1])
print(dic2)