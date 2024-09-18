(module
  (memory $mem 1)
  (export "memory" (memory $mem))

  ;; Define the function signature for sort
  (func (export "sort") (param i32 i32) (result)
    ;; Function body starts here
    (local $arr i32)  ;; Local variable to store the pointer to the array
    (local $length i32)  ;; Local variable to store the length of the array
    (local $i i32)  ;; Loop variable i
    (local $j i32)  ;; Loop variable j
    (local $temp i32)  ;; Temporary variable for swapping

    ;; Initialize local variables with function parameters
    (local.set $arr (local.get 0))  ;; Pointer to the array
    (local.set $length (local.get 1))  ;; Length of the array

    ;; Bubble sort implementation with while loops
    (local.set $i (i32.const 0))  ;; Initialize i = 0
    (block $outer_loop
      ;; Outer loop: while (i < length - 1)
      (loop $inner_loop
        ;; Inner loop: while (j < length - i - 1)
        (local.set $j (i32.const 0))  ;; Initialize j = 0
        (block $inner_loop_cond
          (br_if $inner_loop_cond  ;; Equivalent to 'while' condition check
            (i32.lt_s (local.get $j) (i32.sub (local.get $length) (i32.add (local.get $i) (i32.const 1)))))
          ;; Inside inner loop
          ;; Load arr[j] and arr[j+1] into stack
          (i32.load (local.get $arr))
          (i32.load (i32.add (local.get $arr) (i32.const 4)))
          (if (i32.gt_u)  ;; If (arr[j] > arr[j+1])
            (then
              ;; Swap arr[j] and arr[j+1]
              (local.get $arr)  ;; Load arr[j] address
              (i32.load)  ;; Load value of arr[j]
              (local.get $arr)  ;; Load arr[j+1] address
              (i32.load)  ;; Load value of arr[j+1]
              (i32.store (i32.add (local.get $arr) (i32.const 4)))  ;; Store value of arr[j] into arr[j+1]
              (i32.store (local.get $arr))  ;; Store value of arr[j+1] into arr[j]
            )
          )
          ;; Increment j
          (local.set $j (i32.add (local.get $j) (i32.const 1)))
          ;; Continue inner loop
          (br $inner_loop_cond)
        )
        ;; Increment i
        (local.set $i (i32.add (local.get $i) (i32.const 1)))
        ;; Continue outer loop
        (br $outer_loop)
      )
    )
  )
)