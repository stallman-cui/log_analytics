Log Analytics
=============

*** describe: A simple Online log analytics ***

-- Spout is the data source node --

-- Bolt is the data process node --

+ Spout model, the data source node
	* gamelog, read the gamelog data
		- output, for example:
		```python		
		each_gamelog = {
			'op' : {
				'code' : 'login\_logcount',
				'id'   : 1003
			},
			'area' : '549140c8dbdb67794fc0fa3b',
			'ts' : 1420688004,
			'data' : {
				'corpid':2001,
				'type':'signin',
				'server\_name':'server1009',
				'opno':1003,
				'opname':'login\_logcount',
				'acct':'3284681055'
			}
		}
		```
	* payment, get from the payment interface
	  - output, for example:
		```python
	    each_payment = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
		   	'plat' : '2001',
	   		'ts' : 1420646400,
   			'users': {
				'3412825528' : {
					'times' : 1,
			   		'amount' : 2.0
				},
				'3349885891' : {
					'times' : 1,
					'amount' : 1.0
				},
				'1525032152': {
					'amount' : 100.0, 
					'times' : 5
				}, 
				'3429688738': {
					'amount' : 10.0, 
					'times' : 1
				}
			 }
		}
		```

+ Bolt model, the data processing node
	* login:
		- input: the output of the gamelog's login_logcount record
		```python
		each_gamelog = {
			'op' : {
				'code' : 'login\_logcount',
				'id'   : 1003
			},
			'area' : '549140c8dbdb67794fc0fa3b',
			'ts' : 1420688004,
			'data' : {
				'corpid':2001,
				'type':'signin',
				'server\_name':'server1009',
				'opno':1003,
				'opname':'login\_logcount',
				'acct':'3284681055'
			}
		}
		```
		- output:
		```python
		each_login = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
			'plat' : '2001'
			'count' : 1,
			'userlist' : ['3284681055',],
			'type' : 'login',
		}	
		```
	* signup
		- input: the output of the gamelog's signup_logcount record
		```python
		each_gamelog = {
			'op' : {
				'code' : 'signup\_logcount',
				'id'   : 1001
			},
			'area' : '549140c8dbdb67794fc0fa3b',
			'ts' : 1420688004,
			'data' : {
				'corpid':2001,
				'type':'signup',
				'server\_name':'server1009',
				'opno':1001,
				'opname':'signup\_logcount',
				'acct':'3284681055'
			}
		}
		```

		- output:
		```python
		each_signup = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
			'plat' : '2001'
			'count' : 1,
			'userlist' : ['3284681055',],
			'type' : 'signup',
		}	
		```
	* createrole
		- input: the output of the gamelog's createrole record
		```python
		each_gamelog = {
			'op' : {
				'code' : 'createrole\_logcount',
				'id'   : 1001
			},
			'area' : '549140c8dbdb67794fc0fa3b',
			'ts' : 1420688004,
			'data' : {
				'corpid' : 2001,
				'type' : 'createrole',
				'server\_name' : 'server1009',
				'opno' : 1001,
				'opname' : 'createrole\_logcount',
				'acct':'3284681055'
			}
		}
		```

		- output:
		```python
		each_signup = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
			'plat' : '2001'
			'count' : 1,
			'userlist' : ['3284681055',],
			'type' : 'createrole',
		}	
		```
	

	* payorderuser
		- input:  the output of the payment
		```python
	    each_payment = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
		   	'plat' : '2001',
	   		'ts' : 1420646400,
   			'users': {
				'3412825528' : {
					'times' : 1,
			   		'amount' : 2.0
				},
				'3349885891' : {
					'times' : 1,
					'amount' : 1.0
				},
				'1525032152': {
					'amount' : 100.0, 
					'times' : 5
				}, 
				'3429688738': {
					'amount' : 10.0, 
					'times' : 1
				}
			 }
		}
		```
		
		- output:
		```python
		each\_payorderuser = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
		   	'plat' : '2001',
	   		'ts' : 1420646400,
			'count' : 4,
			'userlist' : ['3412825528','3349885891', '1525032152','3429688738'],
			'pay_amout' : 113,
			'pay_count' : 8,
			'type' : 'payorderuser'
		}
		```

	* server
		- input: the output of the login, signup, createrole, payorderuser

		- output:
		```python
		each_server = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
		   	'plat' : '2001',
	   		'ts' : 1420646400,
			'active' : 2,
			'reg' : 1,
			'create_role' : 1,
			'pay_user' : 4,
			'pay_count' : 8,
			'pay_amout' : 113
		}
		```
		
+ Message tuples transfer 
	* Sender, Publish all the message tuples
		- input: read message tuple from the Queue()

		- output: 'tcp://127.0.0.1:5001', publish the message
		  tuple with the topic
		
	* Receiver, Collect all the message tuples
		- input: read the message tuple with 'tcp://127.0.0.1:5000'

		- output: put received message tuple into the Queue()

	* Gamelog Spout, generate gamelog message tuple to Receiver

	* Payment Spout, generate payment message tuple to Receiver

	* Login Bolt,  Read the login\_logcount message tuple from Sender,
	  and send the processed message tuple to Receiver
	  
	* Signup Bolt,  Read the signup\_logcount message tuple from Sender,
	  and send the processed message tuple to Receiver

	* Createrole Bolt,  Read the createrole\_logcount message tuple
	  from Sender, and send the processed message tuple to Receiver

	* Payorderuser Bolt, Read the payment message tuple from Sender,
	  and send the processed message tuple to Receiver

	* Server Bolt, Read the login, signup, createrole, payorderuser
	  message tuple from Sender, and send the processed message tuple
	  to the Receiver

	** the Bolt node will update the mongodb respectively, if they need **

+ Test 

	* test_\read\_payment\_not\_empty, test the payment model can get
	  payment data from the payment interface

	* test\_read\_gamelog\_not\_empty, test the gamelog model can get
	  gamelog data from the remote game servers

	* test\_connect\_to\_mongodb, test the connection with mongodb service

	* test\_signup\_hanle\_data, test the signup model process
	  message body

	* test\_createrole\_hanle\_data, test the createrole model
	  process message body

	* test\_login\_hanle\_data, test the login model process message body

	* test\_payorderuser\_handle_data, test the payorderuser model
	  process message body

	* test\_transfer\_data\_count, test whether all the spout data has
	  been processed by bolt nodes, for example:
	  
	  ```python
	  all_spout_count:  {
		  'payment': 27,
		  'gamelog': 11
	  }
	  
	  all_bolt_count:  {
		  'login': 1,
		  'server': 38,
		  'signup': 5,
		  'createrole': 5,
		  'payorderuser': 27
	  }
	  ```

	 the source messages is 28, login bolt get 1, signup bolt get 5,
	 
	 createrole bolt get 5, payorderuser get 27, the all the login,
	 
	 signup, createrole, payorderuser message tuples is send to server.
	 
	 All the message tuples has been processed.
