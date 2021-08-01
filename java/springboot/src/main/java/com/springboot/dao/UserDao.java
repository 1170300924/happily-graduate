package com.springboot.dao;
 
import java.util.List;

import org.springframework.stereotype.Repository;
 
import com.springboot.bean.User;
 
@Repository
public interface UserDao extends CommonDao<User> {
	List<User> getUserByStudentid(int studentid);
}
