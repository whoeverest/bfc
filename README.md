## The Brainfuck Computer

BFC is:

1. A stack of compilers that compiles a LISP language to Brainfuck code
2. A hardware implementation of a Brainfuck interpreter

In other words, an attempt to make a computer from scratch.

### LISP

```lisp
(if (= 2 3)
    (print 0)
    (print 1))
```

### Stack Machine

```
1. PUSH 3
2. PUSH 2
3. JMPZ 7
4. PUSH 0
5. PRINT
6. JMP 9
7. PUSH 1
8. PRINT
9. END
```

### Brainfuck

```brainfuck
+++---  # Or something like that :)
```
