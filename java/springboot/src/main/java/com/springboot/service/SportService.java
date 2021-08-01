package com.springboot.service;
 
import java.util.List;

import org.springframework.lang.Nullable;

import com.springboot.bean.Sport;
 
public interface SportService {
 
	/**
	 * 保存用户对象
	 * @param sport
	 */
	void save(Sport sport);
	
	@Nullable
	List<Sport> getSportByStudentid(int studentid);
	
}
