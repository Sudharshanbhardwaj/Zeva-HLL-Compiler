(module
  (memory $memory (export "memory") 1)  ;; Define memory with 1 page (64KB)

  (func (export "caesarEncrypt") (param $plaintext i32) (param $plaintextLength i32) (param $key i32)
    (local $i i32)
    (local.set $i (i32.const 0))

    (block $encryptLoop
      (loop $encryptLoopBody
        (i32.ge_u (local.get $i) (local.get $plaintextLength))
        br_if $encryptLoopBody

        ;; Encrypting formula: (plaintext[i] + key) % 26
        (i32.load8_u (i32.add (local.get $plaintext) (local.get $i))) ;; Load plaintext[i]
        (local.get $key) ;; Load key
        (i32.add) ;; Add key to plaintext[i]
        (i32.const 26) ;; Modulus operand
        (i32.rem_u) ;; Modulus operation with 26
        (i32.store8 (i32.add (local.get $plaintext) (local.get $i))) ;; Store the result back to plaintext[i]

        (local.set $i (i32.add (local.get $i) (i32.const 1))) ;; Increment i
        br $encryptLoop ;; Continue looping
      )
    )
  )

  (func (export "caesarDecrypt") (param $plaintext i32) (param $plaintextLength i32) (param $key i32)
    (local $i i32)
    (local.set $i (i32.const 0))

    (block $decryptLoop
      (loop $decryptLoopBody
        (i32.ge_u (local.get $i) (local.get $plaintextLength))
        br_if $decryptLoopBody

        ;; Decrypting formula: (plaintext[i] - key + 26) % 26
        (i32.load8_u (i32.add (local.get $plaintext) (local.get $i))) ;; Load plaintext[i]
        (local.get $key) ;; Load key
        (i32.sub) ;; Subtract key from plaintext[i]
        (i32.const 26) ;; Add 26 to ensure positive result
        (i32.add) ;; Add 26 to ensure positive result
        (i32.const 26) ;; Modulus operand
        (i32.rem_u) ;; Modulus operation with 26
        (i32.store8 (i32.add (local.get $plaintext) (local.get $i))) ;; Store the result back to plaintext[i]

        (local.set $i (i32.add (local.get $i) (i32.const 1))) ;; Increment i
        br $decryptLoop ;; Continue looping
      )
    )
  )
)