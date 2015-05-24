
"""
push 1
push 2
push 3
multiply
add
push 4
add
"""

"""
+>
++>
+++>
 multiply code here -> memory = [1, 6, _]
                                       ^
 add code here -> memory = [7, _]
                               ^
++++>
 add code here -> memory = [11, _]
                                ^
"""

"""
(print (* (+ 2 3) (- 5 2)))
(function (x y) (+ x y))

push 3 [3]
push 2 [3, 2]
add [5]
push 2 [5, 2]
push 5 [5, 2, 5]
sub [5, 3]
multiply [15]
print
"""

"""
(if (== 10 5)
    (print 0)
    (print 1))

1. push 5
2. push 10
3. equals
4. jmp_if_one, 7
5. push 0
6. print
7. push 1
8. print
"""
from petting import cmpl
from brainfuck import Brainfuck

class Stack(object):
    def __init__(self):
        pass

    def _sp(self):
        # note: you end up in value space after M,
        # not address.
        return 'M}[>]}'

    def _widen(self):
        # Mark next address to be current sp and move to the new sp value"
        return '{+>-}'

    def _squeeze(self):
        return '{+<-}'

    def push_const(self, value):
        "Push a constant to the stack."
        return self._sp() + '[-]' + ('+' * value) + self._widen()

    def pop(self):
        return self._sp() + self._squeeze()

    def equals(self):
        """ Check if the two topmost values on the stack are equal.
        If they are, push 1. Otherwise, push 0.
        """
        pass

s = Stack()
code = s.push_const(5) + s.pop() + s.push_const(4)
compiled = cmpl(code)
print code
print compiled
b = Brainfuck(compiled)
b.run(print_state=True, sleep_time=0.02)
print 'asdsadasdasdas'
print b.memory
print 'asd'