
package com.springboot.service;
 
import java.util.List;

import org.springframework.lang.Nullable;

import com.springboot.bean.Sportuse;
 
public interface SportuseService {
 
	/**
	 * 保存用户对象
	 * @param sportuse
	 */
	void save(Sportuse sportuse);
	
	@Nullable
	List<Sportuse> getSportuseByStudentid(int studentid);
	
}
