def consumer():
    r = 'yield'
    while True:
        print('[CONSUMER] r is %s...' % r)
        #当下边语句执行时，先执行yield r，然后consumer暂停，此时赋值运算还未进行
        #等到producer调用send()时，send()的参数作为yield r表达式的值赋给等号左边
        n = yield r #yield表达式可以接收send()发出的参数
        if not n:
            return # 这里会raise一个StopIteration
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)   #调用consumer生成器
        print('[PRODUCER] Consumer return: %s' % r)
    c.send(None)    
    c.close()

c = consumer()
produce(c)