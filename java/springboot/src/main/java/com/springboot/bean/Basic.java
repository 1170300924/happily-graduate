package com.springboot.bean;

import java.sql.Date;

import javax.persistence.Entity;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;

 
@Entity
@Table(name = "basic")
@Getter
@Setter
public class Basic extends BaseBean {
 
	private int studentid;

	private String name;
	private String sex;
	private String institute;
	private String major;
	private String detail;
	private String nat;
	private String pol;
	private Date birth;
	private String home;
	
}