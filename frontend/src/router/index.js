import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

import memberList from '@/components/member/memberList'
import memberDetail from '@/components/member/memberDetail'
import memberAdd from '@/components/member/memberAdd'
import adminRoles from '@/components/member/adminRoles'

import groupsLanding from '@/components/groups/groupsLanding'
import groupList from "@/components/groups/groupList"
import groupDetail from "@/components/groups/groupDetail"
import randomMessage from "@/components/groups/randomMessage"

import events from "@/components/events/events"
import eventDetail from '@/components/events/eventdetail'

import projectList from "@/components/projects/projectList"
import projectDetail from "@/components/projects/projectDetail"
import importPledgesFromCSV from "@/components/projects/importPledgesFromCSV"

import generalFinance from "@/components/finance/generalFinance"
import income from "@/components/finance/income"
import expenditure from "@/components/finance/expenditure"

import  dailyVerse from "@/components/daily-verses/dailyVerse"
import sermons from "@/components/sermons/sermons"
import services from "@/components/services/services"
import serviceBookings from "@/components/services/serviceBookings"

import login from "@/components/auth/login"
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login/',
      name: 'login',
      component: login
    },
    {
      path: '/reset-credentials/',
      name:'credentialsReset',
      component: () => import("@/components/auth/credentialsReset.vue")
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/memberList',
      name: 'memberList',
      component: memberList
    },
    {
      path: '/memberDetail/:id',
      name: 'memberDetail',
      component: memberDetail
    },
    {
      path: '/memberAdd/',
      name: 'memberAdd',
      component: memberAdd
    },
    {
      path: '/adminRoles',
      name: 'adminRoles',
      component: adminRoles
    },
    {
      path: 'groupsLanding',
      component: groupsLanding,
      children: [
        {
          path: '',
          name: 'groupsLanding',
          component: groupList
        },
        {
          path: '/groupList/:id/:group_name',
          name: 'groupList',
          component: groupList
        }
      ]
    },
    {
      path:'/groupDetail/:id/',
      name: 'groupDetail',
      component: groupDetail
    },
	{
	  path:'/randomMessage/',
	  name: 'randomMessage',
	  component: randomMessage
	},
    {
      path:'/events/',
      name: 'events',
      component: events
    },
    {
    path: '/eventDetail/:id',
    name: 'eventDetail',
    component: eventDetail
    },
    {
      path:'/projectList/',
      name:'projectList',
      component: projectList
    },
    {
      path: '/projectDetail/:id/',
      name: 'projectDetail',
      component: projectDetail
    },
	{
	  path: '/importPledgesFromCSV/',
	  name: 'importPledgesFromCSV',
	  component: importPledgesFromCSV
	},
    {
      path: '/generalFinance/',
      name: 'generalFinance',
      component: generalFinance
    },
    {
      path: '/income/:id',
      name: 'income',
      component: income
    },
    {
      path: '/expenditure/:id',
      name: 'expenditure',
      component: expenditure
    },
    {
      path: '/dailyVerse/',
      name: 'dailyVerse',
      component: dailyVerse
    },
    {
      path: '/sermons/',
      name: 'sermons',
      component: sermons
    },
    {
      path: '/services/',
      name: 'services',
      component: services
    },
    {
      path: '/service-bookings/:id',
      name: 'service-bookings',
      component: serviceBookings
    },
    {
      path: '/sms-analytics/',
      name: 'smsAnalytics',
      component:  () => import('@/components/sms/smsAnalytics.vue')
    },
    {
      path: '/my-account/',
      name: 'myAccount',
      component:  () => import('@/components/account/myAccount.vue')
    },
    {
      path: '/news/',
      name: 'news',
      component:  () => import('@/components/news/news.vue')
    },
    {
  path: '/sms',
  name: 'sms',
  component: () => import('@/components/sms/SmsGroupSender.vue')
},
{
  path: '/csvupload',
  name: 'csvupload',
  component: () => import('@/components/member/Csvimport.vue')
}
  ]
})
