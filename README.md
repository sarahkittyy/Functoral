# Functorial

A *purely* functional programming language.

## Syntax

```
!! This is a comment

!! Function definition:
!! name(param1,param2..) { expr }

sum(x, y, z) { [+ x [+ y z]] }
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! Expressions
!!
!! Expressions are composed of inside square brackets,
!! in which the amount of parameters depends on the context.
!! Ex:
!! [+ y z]
!! [* x 2]
!! [- 2 1]
!! [/ 5 4]
!! [x]
!! [5]
!! [& 1 0] !! << & Operator executes both statements, but only returns the first's value.
!!
!! Expressions can be nested.
!! Ex: [* 2 [* 2 2]]
!! 
!! [noop] indicates nothing to be done.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! Param properties.
!!
!! Syntax:
!! <prop>paramName  
!!
!! Properties:
!! <in> - Takes console input on current line, as number, 
!! and puts it into the variable name.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! Method properties.
!!
!! Same syntax as param properties.
!!
!! Properties:
!! <out> - Outputs function's return value.
!! Ex: 

get(<in>x)
{ !! newlines / whitespace is irrelevant
	[x]}
<out>output(x) { [x] }

!! Calling functions:

output(get())		!! <in> tagged variables do not have to be passed.
					!! Alternatively, pass a value to be used if the input is invalid (defaults to 0)
					
!! Printing strings:

print(Input a number!) !! print is built-in-- only accepts raw text
output(get())

!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! Conditionals
!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!
get(<in> x){[? [cond] [true false]]}

!! Conditional Expression Format
!!
!! [oper val val]
!! Operators are C-Style
!! Ex:
!! [== 2 2]
!! [<= x 8]
!! [!= y x]
!!
!! True-False expression Format
!! [val-if-true val-if-false]

!! Examples:
check_five(x){[? [== x 5] [1 0]]}

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! Calling from expressions
!!
!! Wrap the call in regex begin-end notation: ^...$ so the
!! interpreter knows it's a call & returns a regular value.
!!
factorial(x){[? [<= x 1] [1 [* x ^factorial([- x 1])$]]]}
```

## Notes

All functions are read & initialized before code execution. Ex:
```
> Enter a number:
output(get())

get(<in>x){[x]}
<out>
output(x){[x]}
```