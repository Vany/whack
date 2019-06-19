package main

import (
	"net/http"
	"os"
	"os/exec"
	"strconv"
	"time"
)


var last_data = time.Now()
var cache_time = time.Duration(1 *time.Minute)
var data_cache []byte
var command = "../api_agent.py"

func MHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Write(data_cache)
}

func fetcher() {
	out, err := exec.Command("python3" , command).Output()
	if err!=nil {
		data_cache = []byte(`[{"name":"error", "bonus":10, "latitude": 0, "longitude": 0}]`)
		return
	}
	data_cache = out
}


func main() {

	go func() {
		for {
			fetcher()
			time.Sleep(cache_time)
		}
	}()

	http.HandleFunc("/", MHandler)
	port, ok := os.LookupEnv("HTTP_PORT")
	if !ok { port = "8010"}

	_, err := strconv.Atoi(port)
	if err != nil {
		panic("not numeric port")
	}

	err = http.ListenAndServe(":" + port, nil) // задаем слушать порт
	if err != nil {
		panic("ListenAndServe: "+ err.Error())
	}
}
