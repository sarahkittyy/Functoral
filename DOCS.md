# Functoral Docs

## Comments

```
!! This is a comment
```

---

## Function declarations

### Syntax
```
<tag1><tag2>name(<ptag1><ptag2>param1...) { body... }
!! Whitespace is irrelevant.
```

### Function Tags

These are predefined tags appendable to functions to give them properties.

Avaliable Tags:

| Tag | Description |
|-|-|
| `<out>` | Makes the function print its return value. |

### Parameter Tags

Mark certain parameters as having certain properties.

Avaliable tags:

| Tag | Description |
|-|-|
| `<in>` | The method will attempt to take console input for this value.<br>If the input is invalid, it will use the passed value. |

### Function Body

Composed of a single expression. Other expressions are ignored.

See `Expressions` down below.

---

## Expressions

Expressions are defined as whitespace-delimted parameters inside square brackets `[ ]`.

Expressions can be nested.

There are four types of expressions:

### Identity Expressions

Composed of a single variable/literal inside the square brackets.

Ex:
`[1]` returns 1. `[x]` returns the value inside x.

### Arithmetic Expressions

Composed of an operator, and two values to operate on.

Syntax: `[oper lvalue rvalue]`

Avaliable operators:

| Operator | Function |
|-|-|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `&` | Interprets both values,<br>but returns the left one. |

Ex:
```
[- 5 4] !! Returns 1
[+ 2 3] !! Returns 5
[* [+ 2 4] 6] !! Returns 36
[& 8 9] !! Returns 8
```

### Conditional Expressions

Composed of a comparative operator, and the two values to test. Returns True / False (1 / 0)

Same syntax as arithmetic expressions.

Avaliable operators:

| Operator | Function |
|-|-|
| `==` | True if equal. |
| `!=` | True if not equal. |
| `<` | Less than. |
| `>` | Greater than. |
| `<=` | Less than or equal to. |
| `>=` | Greater than or equal to. |

Examples:

```
[<= 2 3] !! True
[>= 5 5] !! True
[!= 3 3] !! False
[== [<= 1 2] 1] !! True
```

### Fork Expressions

Defined by an initial `?` operator.

Syntax:

`[? condition options]`

The condition is itself an expression, that returns 1 / 0 (True / False).. (See `Conditional Expressions`)

The options expression is a two-parameter expression formatted as:

`[value-if-true value-if-false]`

Examples:
```
[?
	[<= 4 3] !! Expr returns False
	[
		5 !! if-true
		4 !! if-false
	]
] !! Returns 4
[?
	[== 3 3] !! True
	[
		[* 3 3] !! if-true
		[+ 3 3] !! if-false
	]	
] !! Returns 9
```

Note that only one of the true/false branches will be evaluated.

---

## Nesting

Expressions can nest other expressions, as well as other method calls.

The return value from either an expression or method can be used inside other expressions/methods.

Method calls must be wrapped in ^...$ symbols inside expressions, but not other calls.

Examples:
```
inc(x){[+ x 1]}
inc(4) !! Five
inc([+ 1 3]) !! Five 
inc(inc(2)) !! Four

[* 2 ^inc(1)$] !! Four
[/ 10 ^inc(4)$] !! Two

[+ 
	^inc( !! 8
		inc( !! 7
			[+ 2 4] !! 6
		)
	)$ 
	^inc( !! 4
		[+ 1 ^inc(1)$] !! 3
	)$
] !! Returns 12
``` 