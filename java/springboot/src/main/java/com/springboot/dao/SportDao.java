package com.springboot.dao;
 
import java.util.List;

import org.springframework.stereotype.Repository;

import com.springboot.bean.Sport;
 
@Repository
public interface SportDao extends CommonDao<Sport> {
	List<Sport> getSportByStudentid(int studentid);
}
