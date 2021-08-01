
package com.springboot.bean;
 
import javax.persistence.Entity;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;

 
@Entity
@Table(name = "myout")
@Getter
@Setter
public class User extends BaseBean {
 
	private int studentid;
	
	private Integer grade;
	private Integer sport;
	private Integer social;
	private Integer regular;
	private Integer hard;
	private Integer reading;
	
	private String gradeword;
	private String sportword;
	private String socialword;
	private String regularword;
	private String hardword;
	private String readword;
	private String hobbyword;
	private String alertgk;
	private String alertpo;
	private String moocword;
	private String codeword;
}