package com.springboot.controller;
 
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.springboot.bean.Basic;
import com.springboot.bean.Sport;
import com.springboot.bean.Sportuse;
import com.springboot.bean.User;
import com.springboot.service.BasicService;
import com.springboot.service.SportService;
import com.springboot.service.SportuseService;
import com.springboot.service.UserService;
 
@Controller
public class UserController {

	@Autowired
	private UserService userService;
	@Autowired
	private BasicService basicService;
	@Autowired
	private SportService sportService;
	@Autowired
	private SportuseService sportuseService;
	
	@RequestMapping("/hello")
	@ResponseBody
	public String hello() {
		return "Hello World  ABCdfe";
	}
	@RequestMapping("/index")
	
	public String index(Model model) {
		return "index";
	}
	
	@RequestMapping("/userList")
	public String userList(Model model, @RequestParam(name = "studentid") int studentid) {
		List<User> userList = userService.getUserByStudentid(studentid);
		if(!userList.isEmpty()) {
			List<Basic> basicList = basicService.getBasicByStudentid(studentid);
			model.addAttribute("basic", basicList.get(0));
			User user = userList.get(0);
			//成绩分析
			String[] gradeword1=user.getGradeword().split("@@");
			Float[] scores=new Float[5];
			int i;
			for(i=0;i<5;i++)
			{
				scores[i]=Float.valueOf(gradeword1[i]);
			}
			String[] classes={"数理基础课","专业课","英语课","文化素质课","思想政治课"};
			String gradeword="超擅长";
			for(i=0;i<5;i++)
			{
				if(scores[i].equals(Collections.max(Arrays.asList(scores))))
				{
					gradeword=gradeword+classes[i];
					break;
				}
			}
			gradeword=gradeword+"， 最擅长科目: "+gradeword1[7];
			model.addAttribute("gradeword", gradeword);
			//社交分析
			String[] socialword1=user.getSocialword().split("@@");
			String socialword="最亲密的朋友是"+socialword1[2];
			model.addAttribute("socialword", socialword);
			//规律性分析
			String[] regularword1=user.getRegularword().split("@@");
			Float[] scores2=new Float[3];
			String regularword="最爱";
			String[] rc= {"早上","中午","晚上"};
			for(i=0;i<3;i++)
				scores2[i]=Float.valueOf(regularword1[i+1]);
			for(i=0;i<3;i++)
			{
				if(scores2[i].equals(Collections.max(Arrays.asList(scores2))))
				{
					regularword=regularword+rc[i]+regularword1[i+13]+"吃饭，坚持住哦";
					break;
				}
			}
			model.addAttribute("regularword", regularword);
			//努力维度
			String[] hardword1=user.getHardword().split("@@");
			String hardword="累计在图书馆学习：" +hardword1[0]+"小时，累计在教室学习："+hardword1[4]+"小时，加油哦";
			model.addAttribute("hardword", hardword);
			//阅读量维度
			String[] readingword1=user.getReadword().split("@@");
			String readingword="总共阅读 "+readingword1[0]+"本书，上周阅读 "+readingword1[1]+"本书，您的阅读关键词为："+readingword1[5].split(" ")[0]+" "+readingword1[5].split(" ")[1];
			model.addAttribute("readingword", readingword);
			//兴趣分析
			String hobbyword=user.getHobbyword();
			hobbyword=hobbyword.replaceAll("@@"," ");
			model.addAttribute("hobby", hobbyword);
			
			String alertgk=user.getAlertgk();
			if(alertgk!=null)
			{
				alertgk=alertgk.replaceAll("@@"," ");
				model.addAttribute("alertgk", alertgk);
			}
			else
			{
				model.addAttribute("alertgk", " ");
			}
			model.addAttribute("studentid", user.getStudentid());
			model.addAttribute("user", userList.get(0));
		    return "list";
		}
		else return "index";
	}
	@RequestMapping("/userbasic")
	public String userbasic(Model model, @RequestParam(name = "studentid") int studentid) {
		List<Basic> basicList = basicService.getBasicByStudentid(studentid);
		if(!basicList.isEmpty()) {
	    model.addAttribute("basic", basicList.get(0));
	    return "basic";
		}
		else return "index";
	}
	@RequestMapping("/usersport")
	public String usersport(Model model, @RequestParam(name = "studentid") int studentid) {
		List<Sport> sportList = sportService.getSportByStudentid(studentid);
		List<Sportuse> sportuseList = sportuseService.getSportuseByStudentid(studentid);
		if(!sportList.isEmpty()) {
			Sport sport=sportList.get(0);
			double thousand=Integer.valueOf(sport.getThousand().split(":")[0])*60+Integer.valueOf(sport.getThousand().split(":")[1]);
			thousand=(420-thousand)/(1.8);
			double fifty=(sport.getFifty()-6)/3*100;
			double jump=(sport.getJump()-1.5)*100;
			double yinti=sport.getYinti()*10;
			double qianqu=(sport.getQianqu()+1)/14*(-100);
			Map<String,Integer> hm=new HashMap<>();
			for(Sportuse s:sportuseList)
			{
				if(!hm.containsKey(s.getSport()))
					hm.put(s.getSport(), 0);
				hm.put(s.getSport(), hm.get(s.getSport())+1);
			}
			List<Map.Entry<String,Integer>> list = new ArrayList<Map.Entry<String,Integer>>(hm.entrySet());
			Collections.sort(list,new Comparator<Map.Entry<String,Integer>>() {
	            //升序排序
	            public int compare(Entry<String, Integer> o1,
	                    Entry<String, Integer> o2) {
	                return o2.getValue().compareTo(o1.getValue());
	            }
	            
	        });
			String s="去运动场馆"+String.valueOf(sportuseList.size())+"次，最喜爱去"+list.get(0).getKey()+"，曾去过"+String.valueOf(list.get(0).getValue())+"次。";
			model.addAttribute("word",s);
			model.addAttribute("thousand", (int)thousand);
			model.addAttribute("fifty", (int)fifty);
			model.addAttribute("jump", (int)jump);
			model.addAttribute("yinti", (int)yinti);
			model.addAttribute("qianqu", (int)qianqu);
			model.addAttribute("sport", sportList.get(0));
			return "sport";
		}
		else return "index";
	}
	@RequestMapping("/userread")
	public String userread(Model model, @RequestParam(name = "studentid") int studentid) {
		List<User> userList = userService.getUserByStudentid(studentid);
		if(!userList.isEmpty()) {
			User user=userList.get(0);
			String[] s=user.getReadword().split("@@");
			model.addAttribute("reading",user.getReading());
			model.addAttribute("total",s[0]);
			model.addAttribute("lw",s[1]);
			model.addAttribute("book",s[2]+" "+s[3]+" "+s[4]);
			model.addAttribute("gjc",s[5]);
			model.addAttribute("studentid",studentid);
			return "reading";
		}
		else return "index";
	}
	@RequestMapping("/userregular")
	public String userregular(Model model, @RequestParam(name = "studentid") int studentid) {
		List<User> userList = userService.getUserByStudentid(studentid);
		if(!userList.isEmpty()) {
			User user=userList.get(0);
			String[] s=user.getRegularword().split("@@");
			model.addAttribute("regular",user.getRegular());
			model.addAttribute("avg","平均熵值为： "+s[0]);
			model.addAttribute("zaofan","早饭熵值为： "+s[1]);
			model.addAttribute("zaofan2","最早早饭时间： "+s[5]+"   最晚早饭时间： "+s[6]+"   习惯早饭时间： "+s[13]);
			model.addAttribute("wufan","午饭熵值为： "+s[2]);
			model.addAttribute("wufan2","最早午饭时间： "+s[7]+"   最晚午饭时间： "+s[8]+"   习惯午饭时间： "+s[14]);
			model.addAttribute("wanfan","晚饭熵值为： "+s[3]);
			model.addAttribute("wanfan2","   最早晚饭时间： "+s[9]+"   最晚晚饭时间： "+s[10]+"   习惯晚饭时间： "+s[15]);
			model.addAttribute("xizao","洗澡熵值为： "+s[4]);
			model.addAttribute("xizao2","最早洗澡时间： "+s[11]+"   最晚洗澡时间： "+s[12]+"   习惯洗澡时间： "+s[16]);
			model.addAttribute("studentid",studentid);
			return "regular";
		}
		else return "index";
	}
	@RequestMapping("/usergrade")
	public String usergrade(Model model, @RequestParam(name = "studentid") int studentid) {
		List<User> userList = userService.getUserByStudentid(studentid);
		if(!userList.isEmpty()) {
			User user=userList.get(0);
			String[] s=user.getGradeword().split("@@");
			model.addAttribute("xuefen",Float.valueOf(s[5]));
			model.addAttribute("like",Float.valueOf(s[0]));
			model.addAttribute("zhuanye",Float.valueOf(s[1]));
			model.addAttribute("yingyu",Float.valueOf(s[2]));
			model.addAttribute("wenhua",Float.valueOf(s[3]));
			model.addAttribute("sizheng",Float.valueOf(s[4]));
			model.addAttribute("youxiu",s[6]);
			model.addAttribute("studentid",studentid);
			return "grade";
		}
		else return "index";
	}
	
	@RequestMapping("/userhard")
	public String userhard(Model model, @RequestParam(name = "studentid") int studentid) {
		List<User> userList = userService.getUserByStudentid(studentid);
		if(!userList.isEmpty()) {
			User user=userList.get(0);
			String[] s=user.getHardword().split("@@");
			
			model.addAttribute("lab1",s[0]);
			model.addAttribute("lab2",s[1]);
			model.addAttribute("lab3",s[2]);
			model.addAttribute("lab4",s[3]);
			model.addAttribute("cla1",s[4]);
			model.addAttribute("cla2",s[5]);
			model.addAttribute("cla3",s[6]);
			model.addAttribute("cla4",s[7]);
			model.addAttribute("studentid",studentid);
			return "hard";
		}
		else return "index";
	}
	
	@RequestMapping("/usersocial")
	public String usersocial(Model model, @RequestParam(name = "studentid") int studentid) {
		List<User> userList = userService.getUserByStudentid(studentid);
		if(!userList.isEmpty()) {
			User user=userList.get(0);
			String[] s=user.getSocialword().split("@@");
			
			model.addAttribute("f1",s[0]);
			model.addAttribute("f2",s[1]);
			model.addAttribute("f3",s[2]);
			model.addAttribute("f4",s[3]);
			model.addAttribute("f5",s[4]);
			model.addAttribute("f6",s[5]);
			model.addAttribute("f7",s[6]);
			model.addAttribute("f8",s[7]);
			model.addAttribute("studentid",studentid);
			return "social";
		}
		else return "index";
	}
	
	/*
	
	@RequestMapping("/sportana")
	public String sportana(Model model) {
		int studentid;
		for(studentid=1170300101;studentid<1170301099;studentid++)
		{
			List<Sport> sportList = sportService.getSportByStudentid(studentid);
			List<Sportuse> sportuseList = sportuseService.getSportuseByStudentid(studentid);
			List<User> userList = userService.getUserByStudentid(studentid);
			Sport sport=sportList.get(0);
			
			double thousand=Integer.valueOf(sport.getThousand().split(":")[0])*60+Integer.valueOf(sport.getThousand().split(":")[1]);
			thousand=(420-thousand)/(1.8);
			double fifty=(sport.getFifty()-6)/3*100;
			double jump=(sport.getJump()-1.5)*100;
			double yinti=sport.getYinti()*10;
			double qianqu=(sport.getQianqu()+1)/14*(-100);
			double[] arr=new double[]{thousand,fifty,jump,yinti,qianqu};
			String[] name=new String[] {"一千米王者，","五十米王者，","立定跳远高手，","引体向上高手，","坐位体前屈高手，"};
			Arrays.sort(arr);
			double max=arr[0];
			arr=new double[]{thousand,fifty,jump,yinti,qianqu};
			int i;
			String s1="";
			for(i=0;i<5;i++)
			{
				if(arr[i]==max)
				{
					s1=name[i];
					break;
				}
			}
			Map<String,Integer> hm=new HashMap<>();
			for(Sportuse s:sportuseList)
			{
				if(!hm.containsKey(s.getSport()))
					hm.put(s.getSport(), 0);
				hm.put(s.getSport(), hm.get(s.getSport())+1);
			}
			List<Map.Entry<String,Integer>> list = new ArrayList<Map.Entry<String,Integer>>(hm.entrySet());
			Collections.sort(list,new Comparator<Map.Entry<String,Integer>>() {
	            //升序排序
	            public int compare(Entry<String, Integer> o1,
	                    Entry<String, Integer> o2) {
	                return o2.getValue().compareTo(o1.getValue());
	            }
	            
	        });
			int sporttime=sportuseList.size();
			s1=s1+"去运动场馆"+String.valueOf(sportuseList.size())+"次，最喜爱去"+list.get(0).getKey();
			User user=userList.get(0);
			user.setSport((int)(sport.getTestgrade()*0.65+sport.getCoursegrade()*0.3+Math.log(sporttime)));
			user.setSportword(s1);
			userService.save(user);
		}
		return "index";
	}
	*/
}
