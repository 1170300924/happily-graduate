package com.springboot.bean;

import java.sql.Date;

import javax.persistence.Entity;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;

 
@Entity
@Table(name = "sportuse")
@Getter
@Setter
public class Sportuse extends BaseBean {
 
	private int studentid;

	private String sport;
	private String intime;
	private String outtime;
	
}