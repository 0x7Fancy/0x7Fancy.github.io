package main

import (
    "fmt"
    "time"
)

func test(i int) {
    b := make([]byte, 1024 * 1024 * 256)
    fmt.Println("count", i)
    b[100] = '1'
    fmt.Println("out", i)
}

func main() {
    var pause string = ""
    fmt.Scanln(&pause)

    fmt.Println("[start]")

    for i := 0; i < 10; i++ {
        test(i)
        time.Sleep(1 * time.Second)
    }

    for i := 1; i <= 10; i++ {
		time.Sleep(1 * time.Minute)
		fmt.Printf("%d minutes has passed\n", i)
	}

    fmt.Println("[end]")
    fmt.Scanln(&pause)
}
