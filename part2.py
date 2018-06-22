# these should be the only imports you need
import sys
import sqlite3

# write your code here
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

def get_customers():
	conn = sqlite3.connect('Northwind_small.sqlite')
	c = conn.cursor()

	c.execute('SELECT Id, CompanyName FROM Customer')
	
	print("ID       Customer Name")
	for customer in c:
		print(customer[0] + "    " + customer[1])

	conn.close()


def get_employees():
	conn = sqlite3.connect('Northwind_small.sqlite')
	c = conn.cursor()

	c.execute('SELECT Id, FirstName, LastName FROM Employee')

	print("ID       Employee Name")
	for employee in c:
		print(str(employee[0]) + "        " + employee[1] + " " + employee[2])

	conn.close()


def get_orders(order_type, order_id):

	conn = sqlite3.connect('Northwind_small.sqlite')
	c = conn.cursor()
	
	if(order_type == 'cust'):
		customer_name = c.execute("SELECT Customer.ContactName FROM Customer WHERE Customer.Id = ?", (order_id,)).fetchone()[0]
		c.execute("SELECT 'Order'.OrderDate FROM Customer INNER JOIN 'Order' ON Customer.Id = 'Order'.CustomerId WHERE Customer.Id = ?", (order_id,))

		print("Order dates")

		for order in c:
			print(order[0])

	elif(order_type == 'emp'):
		employee_name = c.execute("SELECT Employee.FirstName, Employee.LastName FROM Employee WHERE Employee.Id = ?", (order_id,)).fetchone()
		c.execute("SELECT 'Order'.OrderDate FROM Employee INNER JOIN 'Order' ON Employee.Id = 'Order'.EmployeeId WHERE Employee.LastName = ?", (order_id,))

		print("Order dates")

		for order in c:
			print(order[0])

	conn.close()


command = sys.argv[1]
order_type = "none"

if len(sys.argv) > 2:
	order_type = sys.argv[2]

if command == "customers":
	get_customers()
elif command == "employees":
	get_employees()
elif command == "orders":
	get_orders(order_type[:order_type.find('=')], order_type[order_type.find('=') + 1:])