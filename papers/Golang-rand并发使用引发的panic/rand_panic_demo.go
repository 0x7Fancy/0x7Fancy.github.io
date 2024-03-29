package main

import (
    "math/rand"
    "sync"
    "time"
)

var randSource = NewRandSource()

func NewRandSource() *rand.Rand {
    return rand.New(rand.NewSource(time.Now().UnixNano()))
}

func calcRand() {
    for i := 0; i < 10000; i++ {
        randSource.Intn(1000)
    }
}

func main() {
    wg := sync.WaitGroup{}
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            calcRand()
            wg.Done()
        }()
    }
    wg.Wait()
}
