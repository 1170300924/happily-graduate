package com.springboot.service;
 
import java.util.List;

import org.springframework.lang.Nullable;

import com.springboot.bean.User;
 
public interface UserService {
 
	/**
	 * 保存用户对象
	 * @param user
	 */
	void save(User user);
	
	@Nullable
	List<User> getUserByStudentid(int studentid);
	
}
