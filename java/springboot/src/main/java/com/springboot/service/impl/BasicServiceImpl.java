
package com.springboot.service.impl;
 
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.lang.Nullable;
import org.springframework.stereotype.Service;
 
import com.springboot.bean.Basic;
import com.springboot.dao.BasicDao;
import com.springboot.service.BasicService;
 
@Service
public class BasicServiceImpl implements BasicService {
 
	@Autowired
	private BasicDao basicDao;
	
	@Override
	public void save(Basic basic) {
		basicDao.save(basic);
		
	}
	
	@Override
	@Nullable
	public List<Basic> getBasicByStudentid(int studentid) {
	    return basicDao.getBasicByStudentid(studentid);
	}
	
 
}