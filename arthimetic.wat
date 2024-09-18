(module
  (memory $mem 1)
  (export "memory" (memory $mem))
  ;; Function Definition
(func $add (param $a i32) (param $b i32) (result i32)
    (i32.add
      (local.get $a)
      (local.get $b)
    )
    return
)
  (export "add" (func $add))
  ;; Function Definition
(func $sub (param $a i32) (param $b i32) (result i32)
    (i32.sub
      (local.get $a)
      (local.get $b)
    )
    return
)
  (export "sub" (func $sub))
  ;; Function Definition
(func $mul (param $a i32) (param $b i32) (result i32)
    (i32.mul
      (local.get $a)
      (local.get $b)
    )
    return
)
  (export "mul" (func $mul))
  ;; Function Definition
(func $div (param $a i32) (param $b i32) (result i32)
    (i32.div_s
      (local.get $a)
      (local.get $b)
    )
    return
)
  (export "div" (func $div))
  ;; Function Definition
(func $mod (param $a i32) (param $b i32) (result i32)
    (i32.rem_s
      (local.get $a)
      (local.get $b)
    )
    return
)
  (export "mod" (func $mod))
)