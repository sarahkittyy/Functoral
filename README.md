# Functorial

A *purely* functional programming language.

## Usage

`python functoral.py file`

## Examples

```
factorial(x) !! define a factorial function
{
	[? !! conditional if statement
		[<= x 1] !! condition (x <= 1)
		[
			1 !! if true
			!! if false
			[* x ^factorial([- x 1])$]
		]
	]
}
<out>run(x)
{
	[^factorial(x)$]
}
run(5) !! output :: 120
```

## Documentation

See `DOCS.md` for syntax.