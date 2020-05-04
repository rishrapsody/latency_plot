#! /usr/bin/env python


"""
author=rishrapsody@gmail.com
date=21-Jan-2020

1. Script takes Destination server as Input from user
2. Runs ping to the provided server for mentioned number of count
3. Plots the graph on [x,y] axis and saves the plot as an image.
4. Triggers an email with graph attachment to the Reicever mentioned by user
"""


import ipaddress
import re
import time
import matplotlib.pyplot as plt
import subprocess
import yagmail

def ping_func(ip_to_check, count, size):
	try:
		x = []
		y = []
		new_yplot = 100
		plt.axis([0, count, 0, new_yplot])
		plt.xlabel('Packet Seq Number')
		plt.ylabel('Response Time(ms)')
		plt.title('Ping Latency Graph\nPacket size:{}b  Destination Server:{}'.format(size,ip_to_check))
		seq = 0
		while (seq <= count):
	#		response =  os.system('ping {} -c10 -i{} -s{}'.format(ip_to_check,interval,size))
	#		response_list = ping(ip_to_check, size=100, count=2)
	#		print(response_list._responses)
			cmd = "ping -c1 -W500 -s{} {}".format(size,ip_to_check)
#			print(cmd)
			try:
#				output = str(subprocess.check_output(cmd, shell=True, timeout=1000))
				output =  str(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0])
#				print(output)
				if("0 packets received" in output or "0 received" in output):
#					print("yes")
					print("No response for seq number {}".format(seq))
					x.append(seq)
					y_infinite = 1000
					y.append(y_infinite)
#					print(y)
					seq = seq + 1
					time.sleep(0.5)
					continue
			except Exception as e:
				print(e)

			matches = re.findall(r" time=([\d.]+) ms", output)
#				print(type(matches))
			latency = float(matches[0])
#			print(int(latency))
			
			if(latency > 100):
				if(latency > new_yplot):
					new_yplot = int(latency)
					plt.axis([0, count, 0, new_yplot+20])
			print("Packet seq is {} and RTT is {}".format(seq,str(matches[0])))
			x.append(seq)
			y.append(float(matches[0]))
#			print(y)
			seq = seq + 1
#			x = np.arange(0.,20.,1)
#			y = np.arange(0.,20.,1)
			
			
#			plt.legend()
#			plt.show()
			time.sleep(1)


		plt.plot(x,y, label='Latency')
		plt.legend()
		
		plt.savefig('latency_graph.png')
#		plt.show()
		plt.close()

	except KeyboardInterrupt:
		print("\n\nOOPS!! Interupted by User")
	
		plt.plot(x,y, label='Latency')
		plt.legend()
		
		plt.savefig('latency_graph.png')
#		plt.show()
		plt.close()
		print("Bye\n\n")
		exit(1)

	except Exception as e:
		print("There is some issue with code")
		print(e)
		exit(1)			


#gather input from User
def gather_inputs():
	

	try:
		ip_to_check = str(ipaddress.IPv4Address(input("Server to ping: ")))

	except Exception as e:
		print("Ran into exception while verifying Server IP. Invalid input")
		exit(1)

	
	while True:
		try:
			count = int(input("Ping count(default is 20): ") or "20")
			if (count <= 30):
				break
			else:
				print("Max limit is 30. Please try again!")
				

		except Exception as e:
			print("Ran into exception while verifying count value. Invalid input")
			exit(1)
	
	try:
		size = int(input("Ping size(default is 64b): ") or "64")

	except Exception as e:
		print("Ran into exception while verifying size. Invalid input")
		exit(1)

	while True:
		try:
			receiver = input("Receiver email id: ").strip()
#			print(receiver)
			regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z]+\.[a-zA-Z.]+$"
			check_email = re.match(regex, receiver)
#			print(check_email)
			if (check_email):
				break
			else:
				print("Invalid input. Try again")
		except Exception as e:
			print("Ran into exception while verifying receiver mail. Invalid input")
			exit(1)

	return(ip_to_check, count, size, receiver)


#trigger email with graph attachment
def send_email(ip_to_check, receiver):
	try:
		body = """
		Hello,

		Please find the attached latency graph for Destination server : {}

		Thank you for using the script.

		Regards,
		BOT
		""".format(ip_to_check)
		filename = "latency_graph.png"

		yag = yagmail.SMTP("python.networkers@gmail.com", "removed password to upload script")
		yag.send(to=receiver, subject = "Latency graph Automated email", contents=body, attachments=filename,)
		time.sleep(1)
		print("\nEmail sent successfully..")

	except Exception as e:
		print("Ran into exception while sending email. Please review your inputs again!!")
		print(e)
		exit(1)




#main function
if __name__ == "__main__":
	ip_to_check, count, size, receiver = gather_inputs()

	ping_func(ip_to_check, count, size)

	send_email(ip_to_check, receiver)