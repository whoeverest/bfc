from .brainfuck import Brainfuck



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