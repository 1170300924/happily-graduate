package com.springboot.bean;

import java.sql.Time;

import javax.persistence.Entity;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;

 
@Entity
@Table(name = "sport")
@Getter
@Setter
public class Sport extends BaseBean {
 
	private int studentid;

	private int testgrade;
	private int coursegrade;
	private String thousand;
	private float fifty;
	private float jump;
	private int yinti;
	private float qianqu;
	
}