package com.springboot.dao;
 
import java.util.List;

import org.springframework.stereotype.Repository;

import com.springboot.bean.Basic;
 
@Repository
public interface BasicDao extends CommonDao<Basic> {
	List<Basic> getBasicByStudentid(int studentid);
}
