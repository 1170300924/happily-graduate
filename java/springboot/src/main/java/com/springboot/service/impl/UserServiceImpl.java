
package com.springboot.service.impl;
 
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.lang.Nullable;
import org.springframework.stereotype.Service;
 
import com.springboot.bean.User;
import com.springboot.dao.UserDao;
import com.springboot.service.UserService;
 
@Service
public class UserServiceImpl implements UserService {
 
	@Autowired
	private UserDao userDao;
	
	@Override
	public void save(User user) {
		userDao.save(user);
		
	}
	
	@Override
	@Nullable
	public List<User> getUserByStudentid(int studentid) {
	    return userDao.getUserByStudentid(studentid);
	}
	
 
}