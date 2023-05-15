## E Store

# Technology
- Database: Mongo - Done
- Backend : Flask - (80 %- 90%)
- Frontend: Nextjs React - <50%

# Backend routes:

PRODUCT
```		
URL                 method	description
/api/product        GET	    Get all products
/api/product/<id>	GET	    Get detail product
```

USER

```			
URL	                method	description
/api/user/signup	POST    Sign up new user 
/api/user/signin	POST    Sign in with account
/api/user/activate  POST    Activate account after signup
```
	
ADMIN
```		
URL                 method	description
/api/admin/signin   POST	Sign in admin account
/api/admin/getuser  POST    Get user in store
```