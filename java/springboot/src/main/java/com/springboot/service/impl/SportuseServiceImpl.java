package com.springboot.service.impl;
 
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.lang.Nullable;
import org.springframework.stereotype.Service;
 
import com.springboot.bean.Sportuse;
import com.springboot.dao.SportuseDao;
import com.springboot.service.SportuseService;
 
@Service
public class SportuseServiceImpl implements SportuseService {
 
	@Autowired
	private SportuseDao sportuseDao;
	
	@Override
	public void save(Sportuse sportuse) {
		sportuseDao.save(sportuse);
		
	}
	
	@Override
	@Nullable
	public List<Sportuse> getSportuseByStudentid(int studentid) {
	    return sportuseDao.getSportuseByStudentid(studentid);
	}
	
 
}