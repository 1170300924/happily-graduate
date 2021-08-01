package com.springboot.service;
 
import java.util.List;

import org.springframework.lang.Nullable;

import com.springboot.bean.Basic;
 
public interface BasicService {
 
	/**
	 * 保存用户对象
	 * @param user
	 */
	void save(Basic basic);
	
	@Nullable
	List<Basic> getBasicByStudentid(int studentid);
	
}
