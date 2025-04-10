from zmapsdk.api import APIServer

if __name__ == "__main__":
    server = APIServer()
    print("Starting ZMAP API server..")
    server.run()


# curl -X POST http://localhost:8000/scan-sync -H "Content-Type: application/json" -d '{"target_port": 80, "subnets": ["192.168.1.0/24"], "return_results": true}'
