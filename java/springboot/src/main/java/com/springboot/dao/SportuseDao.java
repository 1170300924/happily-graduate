package com.springboot.dao;
 
import java.util.List;

import org.springframework.stereotype.Repository;

import com.springboot.bean.Sportuse;
 
@Repository
public interface SportuseDao extends CommonDao<Sportuse> {
	List<Sportuse> getSportuseByStudentid(int studentid);
}
