(module
  (memory $mem 1)
  (export "memory" (memory $mem))
  ;; Function Definition
(func $caesarEncrypt (param $plaintext i32) (param $plaintextLength i32) (param $key i32) 
    ;; Declaration
      (local $i int)
      i32.const 0
      (local.set $i)
    ;; While Statement
      (block $encryptLoop
        (loop $encryptLoopBody
          (local.get $i)
          (local.get $plaintextLength)
          i32.<
          i32.eqz
          br_if $encryptLoopEnd
          ;; Declaration
            (local $result1 int)
            ;; Assignment
              (i32.load8_u (i32.add local.get ($plaintext) local.get ($i)))
            (local.set $result1)
          ;; Assignment
            (i32.rem_s
              (i32.add
                (local.get $result1)
                (local.get $key)
              )
              i32.const 26
            )
          ;; Assignment
            (local.get $result1)
          ;; Assignment
            (i32.add
              (local.get $i)
              i32.const 1
            )
        
        (br $encryptLoop)
      
    
    (br $encryptLoop)
    
  return
)
(export "caesarEncrypt" (func $caesarEncrypt))
;; Function Definition
(func $caesarDecrypt (param $plaintext i32) (param $plaintextLength i32) (param $key i32) 
  ;; Declaration
    (local $i int)
    i32.const 0
    (local.set $i)
  ;; While Statement
    (block $encryptLoop
      (loop $encryptLoopBody
        (local.get $i)
        (local.get $plaintextLength)
        i32.<
        i32.eqz
        br_if $encryptLoopEnd
        ;; Declaration
          (local $result2 int)
          ;; Assignment
            (i32.load8_u (i32.add local.get ($plaintext) local.get ($i)))
          (local.set $result2)
        ;; Assignment
          (i32.rem_s
            (i32.add
              (i32.sub
                (local.get $result1)
                (local.get $key)
              )
              i32.const 26
            )
            i32.const 26
          )
        ;; Assignment
          (local.get $result2)
        ;; Assignment
          (i32.add
            (local.get $i)
            i32.const 1
          )
      
      (br $encryptLoop)
    
  
  (br $encryptLoop)
  
return
)
(export "caesarDecrypt" (func $caesarDecrypt))
)