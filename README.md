Log Analytics
=============

describe: A simple Online log analytics
---------------------------------------

#### Analytics is a coroutine-based log analysis, synchronous user information and 
#### payment data system. It powered by gevent.###

Dependencies
------------
  - gevent: http://www.gevent.org/
  
  - zmq: http://zeromq.org/
  
  - etcd: https://github.com/coreos/etcd
  
  - python-etcd: https://github.com/jplana/python-etcd

Deploy
-----
  [root] ./deploy.sh
  
  service analytics [start|stop|restart]

Module
------
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
	* syncuser, get from the orignal game user data
	  - output, for example:
		```python
		each\_user = {
			'game' : 'wsdx',
			'area' : '54598574dbdb677b6226a5df',
		   	'plat' : '1059',
	   		'ts' : 1423213068,
			'uid' : '141560631361753593',
			'name' : 'superman',
			'grade' : 3,
			'rest_yuanbao' : 200,
			'birthday' : 1418637569,
			'acctid' : kutheso@hotmail.com",
			'score' : 930,
			'login_time' : 1418888736
	    }
        ```

+ Bolt model, the data processing node
	* loginhour:
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
		each_loginhour = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
			'plat' : '2001'
			'ts' : 1420686000,
			'count' : 1,
			'userlist' : ['3284681055',],
			'type' : 'login',
		}	
		```
	* loginday:
	  - input: the output of the loginhour
	  - output:
	  ```python
	  each_loginday = {
		  'game' : 'dl',
		  'area' : '549140c8dbdb67794fc0fa3b',
		  'plat' : '2001'
		  'ts' : 1420646400,
		  'count' : 1,
		  'userlist' : ['3284681055',],
		  'type' : 'login',
	  }
      ```

	* signuphour
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
		each_signuphour = {
			'game' : 'dl',
			'area' : '549140c8dbdb67794fc0fa3b',
			'plat' : '2001'
			'count' : 1,
			'userlist' : ['3284681055',],
			'type' : 'signup',
		}	
		```
	* signupday
	  - input: the output of the signuphour
	  
	  - output: just like login, the different with signuphour is ts
	  
	* createrolehour
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
	* createroleday
	  
	* paysummary
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

	* activeday(timer bolt)
	  - input: read the mongodb's collections server, get the data of today
	  - output:
		```python
		each\_day = {
			'game' : 'wsdx',
			'area' : '5461bb1bec8b9c686a8b4576',
			'plat' : '1059',
			'ts' : 1420646400,
			'ac\_user' : 214,
			'new\_ac\_user' : 109,
			'new\_ac\_rate' : 50.93,
			'old\_ac\_user' : 105,
			'old\_ac\_rate' : 49.07,
	    }
	    ```
	* activeweek(timer bolt)
	
	* activemonth(timer bolt)

	* serverstarttime(timer bolt)

	* coinhour
	  statistics the user comsumed yuanbao

	* coinday

	* cointype
	  statistics the user comsumed yuanbao type

	* gamecopy
	  statistics the fuben_logchange

	* loginretention
	  statistics the user login retention

	* mainline
	  statistics the trunk\_task\_accept and trunk\_task\_finish

	* payorderdetail
	  statictis the every payorder 

	* paytraceday
	  statistics the payment retention

	* shop
	  statistics the user buyed items

	* userpay
	  statistics the user payment info, and yuanbao data

	* usercenter
	  store the user data from remote

	* userlevel
	  statistics the user level distributed

+ Message tuples transfer

	***
		1. Every spout publish the message tuple with it's state,
		
		and most of bolts subscribe message tuple they interested.
		
		2. Timer bolt is special, will read the data from mongodb, and it will
		
		   pushlish the message tuple if necessary.
	***
	Some Exaples:
	
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

Fault Tolerant
--------------
	* store gamelog: before hanle the gamelog data, store the log to disk,
	  if system is going wrong:
		  ```shell
		  cat data/gamelog_201502061738.txt | ./bin/read_stdin_gamelog
		  ```
	* filter bolt: to void count repeat data, ignore the repeat record,
	  just handle the effective message tuple

	* in distribute mode, the etcd service will monitor the system state

Test
----
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
