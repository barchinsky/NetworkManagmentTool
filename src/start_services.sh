python src/SocketServer.py &
echo 'Socket server started.' &
python src/ServiceSimulator.py &
echo 'Service simulator satrted.'
python src/trapreciver.py
echo 'Trap reciever started'
python src/TrapGen.py
echo 'Trap generator started'
