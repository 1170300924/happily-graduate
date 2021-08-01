
package com.springboot.service.impl;
 
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.lang.Nullable;
import org.springframework.stereotype.Service;
 
import com.springboot.bean.Sport;
import com.springboot.dao.SportDao;
import com.springboot.service.SportService;
 
@Service
public class SportServiceImpl implements SportService {
 
	@Autowired
	private SportDao sportDao;
	
	@Override
	public void save(Sport sport) {
		sportDao.save(sport);
		
	}
	
	@Override
	@Nullable
	public List<Sport> getSportByStudentid(int studentid) {
	    return sportDao.getSportByStudentid(studentid);
	}
	
 
}