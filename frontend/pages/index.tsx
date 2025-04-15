import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import { 
  LayoutDashboard, 
  FileText, 
  User, 
  Settings, 
  Sparkles, 
  BarChart2, 
  PieChart as PieChartIcon, 
  Star, 
  Clock, 
  CreditCard,
  TrendingUp,
  Filter,
  Download,
  Save,
  ChevronRight,
  Plus
} from 'lucide-react';

// 샘플 데이터
const weeklyData = [
  { name: '월', value: 12 },
  { name: '화', value: 19 },
  { name: '수', value: 15 },
  { name: '목', value: 27 },
  { name: '금', value: 32 },
  { name: '토', value: 10 },
  { name: '일', value: 8 },
];

const channelData = [
  { name: '인스타그램', value: 35 },
  { name: '페이스북', value: 25 },
  { name: '유튜브', value: 20 },
  { name: '블로그', value: 15 },
  { name: '기타', value: 5 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const historyData = [
  { id: 1, title: '스킨케어 제품 리뷰 분석', date: '2025.04.14', status: '완료' },
  { id: 2, title: '운동 앱 사용자 후기 분석', date: '2025.04.12', status: '완료' },
  { id: 3, title: '식품 브랜드 커뮤니티 분석', date: '2025.04.10', status: '완료' },
];

const creditHistory = [
  { id: 1, type: '분석 사용', amount: -1, date: '2025.04.14 12:30', balance: 19 },
  { id: 2, type: '크레딧 충전', amount: 10, date: '2025.04.10 18:22', balance: 20 },
  { id: 3, type: '분석 사용', amount: -1, date: '2025.04.08 09:45', balance: 10 },
];

// 메인 컴포넌트
const IntrixApp = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(true);
  const [currentTab, setCurrentTab] = useState('analyze');
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* 헤더 네비게이션 */}
      <nav className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <div className="flex items-center">
            <div className="text-xl font-bold text-indigo-600 mr-8">Intrix</div>
            {isLoggedIn && (
              <div className="hidden md:flex space-x-4">
                <button onClick={() => setCurrentTab('analyze')} 
                  className={`px-3 py-2 ${currentTab === 'analyze' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-600'}`}>
                  분석
                </button>
                <button onClick={() => setCurrentTab('mypage')} 
                  className={`px-3 py-2 ${currentTab === 'mypage' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-600'}`}>
                  마이페이지
                </button>
                <button onClick={() => setCurrentTab('admin')} 
                  className={`px-3 py-2 ${currentTab === 'admin' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-600'}`}>
                  관리자
                </button>
              </div>
            )}
          </div>
          {isLoggedIn ? (
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="px-3 py-1.5 bg-gray-50">
                <CreditCard className="w-4 h-4 mr-1" /> 크레딧: 19
              </Badge>
              <Avatar className="h-8 w-8">
                <AvatarImage src="" />
                <AvatarFallback className="bg-indigo-100 text-indigo-600">KM</AvatarFallback>
              </Avatar>
            </div>
          ) : (
            <div className="flex items-center space-x-3">
              <Button variant="outline">로그인</Button>
              <Button>회원가입</Button>
            </div>
          )}
        </div>
      </nav>

      <div className="container mx-auto p-4">
        {/* 로그인 상태에 따른 화면 분기 */}
        {isLoggedIn ? (
          <>
            {currentTab === 'analyze' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                  <h2 className="text-2xl font-bold mb-4">AI 마케팅 전략 분석</h2>
                  <p className="text-gray-600 mb-6">리뷰 또는 커뮤니티 데이터를 분석하여 최적의 마케팅 전략을 도출합니다.</p>
                  
                  <Tabs defaultValue="text-input" className="w-full">
                    <TabsList className="mb-4">
                      <TabsTrigger value="text-input">텍스트 입력</TabsTrigger>
                      <TabsTrigger value="file-upload">파일 업로드</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="text-input" className="space-y-4">
                      <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                        <textarea 
                          className="w-full h-40 p-3 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500" 
                          placeholder="분석할 리뷰 또는 커뮤니티 텍스트를 입력하세요..."
                        />
                      </div>
                      
                      <div className="flex items-center gap-3">
                        <Button className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700">
                          분석 시작하기 <ChevronRight className="w-4 h-4 ml-1" />
                        </Button>
                        <Button variant="outline">샘플 데이터 사용</Button>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="file-upload">
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-10 text-center">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <FileText className="w-10 h-10 text-gray-400" />
                          <p className="text-sm text-gray-500">CSV, Excel, 텍스트 파일을 드래그하거나 클릭하여 업로드하세요</p>
                          <Button variant="outline" size="sm" className="mt-2">파일 선택</Button>
                        </div>
                      </div>
                    </TabsContent>
                  </Tabs>
                </div>
                
                {/* 가상의 분석 결과 표시 섹션 */}
                <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                  <div className="flex justify-between items-center mb-6">
                    <div>
                      <h2 className="text-2xl font-bold">분석 결과</h2>
                      <p className="text-gray-600">스킨케어 제품 리뷰 분석 (2025.04.14)</p>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        <Save className="w-4 h-4 mr-1" /> 저장
                      </Button>
                      <Button variant="outline" size="sm">
                        <Download className="w-4 h-4 mr-1" /> PDF 다운로드
                      </Button>
                      <Button variant="outline" size="sm">
                        <Star className="w-4 h-4 mr-1" /> 즐겨찾기
                      </Button>
                    </div>
                  </div>
                  
                  <Tabs defaultValue="summary">
                    <TabsList className="w-full mb-6">
                      <TabsTrigger value="summary">요약</TabsTrigger>
                      <TabsTrigger value="strategy">전략 추천</TabsTrigger>
                      <TabsTrigger value="branding">브랜딩 전략</TabsTrigger>
                      <TabsTrigger value="execution">실행 전략</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="summary">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <Card>
                          <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-gray-500">주요 감정</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="text-2xl font-bold">신뢰 / 만족감</div>
                            <p className="text-sm text-gray-600 mt-1">78% 비중으로 확인됨</p>
                          </CardContent>
                        </Card>
                        <Card>
                          <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-gray-500">핵심 니즈</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="text-2xl font-bold">안전성 / 효과 검증</div>
                            <p className="text-sm text-gray-600 mt-1">상위 2개 니즈 항목</p>
                          </CardContent>
                        </Card>
                        <Card>
                          <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-gray-500">추천 매체</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="text-2xl font-bold">인스타그램 / 블로그</div>
                            <p className="text-sm text-gray-600 mt-1">전환율 기준 최적 채널</p>
                          </CardContent>
                        </Card>
                      </div>
                      
                      <Card>
                        <CardHeader>
                          <CardTitle>핵심 인사이트</CardTitle>
                          <CardDescription>리뷰 데이터에서 추출한 주요 인사이트입니다.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-100">
                            <div className="font-semibold text-indigo-800 mb-1">안전성에 대한 확신 필요</div>
                            <p className="text-sm text-indigo-700">사용자들은 원료와 성분에 대한 신뢰를 중요시하며, 과학적 검증을 원합니다.</p>
                          </div>
                          <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-100">
                            <div className="font-semibold text-indigo-800 mb-1">지속적 효과에 대한 불확실성</div>
                            <p className="text-sm text-indigo-700">초기 효과는 만족하나 장기적 효과에 대한 의구심이 있습니다.</p>
                          </div>
                          <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-100">
                            <div className="font-semibold text-indigo-800 mb-1">가격 대비 가치 고려</div>
                            <p className="text-sm text-indigo-700">프리미엄 가격에 맞는 차별화된 가치 증명이 필요합니다.</p>
                          </div>
                        </CardContent>
                      </Card>
                    </TabsContent>
                    
                    <TabsContent value="strategy">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {[1, 2, 3, 4, 5, 6, 7].map((item) => (
                          <Card key={item}>
                            <CardHeader>
                              <div className="flex justify-between items-start">
                                <CardTitle className="text-lg">전략 제안 #{item}</CardTitle>
                                <Badge className="bg-indigo-100 text-indigo-800 hover:bg-indigo-200">핵심 전략</Badge>
                              </div>
                              <CardDescription>니즈 분석 기반 추천 전략</CardDescription>
                            </CardHeader>
                            <CardContent>
                              <p className="text-gray-700">
                                과학적 검증 결과를 시각화하여 제품의 안전성과 효과를 명확하게 전달하는 전략을 구사하세요. 
                                성분 함량과 효능에 대한 투명한 정보 제공이 필요합니다.
                              </p>
                            </CardContent>
                            <CardFooter className="border-t pt-4">
                              <Button variant="outline" size="sm" className="w-full">상세 보기</Button>
                            </CardFooter>
                          </Card>
                        ))}
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="branding">
                      <div className="grid grid-cols-1 gap-6">
                        {[1, 2, 3].map((item) => (
                          <Card key={item} className="border-l-4 border-l-indigo-500">
                            <CardHeader>
                              <CardTitle>브랜딩 전략 #{item}</CardTitle>
                              <CardDescription>브랜드 이미지 강화를 위한 제안</CardDescription>
                            </CardHeader>
                            <CardContent>
                              <p className="text-gray-700 mb-4">
                                신뢰와 전문성을 강조하는 브랜드 메시지를 일관되게 유지하세요. 
                                과학적 연구와 전문가 인증을 활용한 신뢰성 구축이 중요합니다.
                              </p>
                              <div className="flex flex-wrap gap-2">
                                <Badge variant="outline">신뢰성</Badge>
                                <Badge variant="outline">전문성</Badge>
                                <Badge variant="outline">투명성</Badge>
                              </div>
                            </CardContent>
                            <CardFooter className="flex justify-between border-t pt-4">
                              <Button variant="outline" size="sm">카피라이팅 예시</Button>
                              <Button size="sm">적용하기</Button>
                            </CardFooter>
                          </Card>
                        ))}
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="execution">
                      <div className="space-y-6">
                        <Card>
                          <CardHeader>
                            <CardTitle>채널별 실행 전략</CardTitle>
                            <CardDescription>각 채널에 최적화된 실행 전략입니다.</CardDescription>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-4">
                              <div className="p-4 bg-gray-50 rounded-lg">
                                <div className="font-semibold mb-2">인스타그램</div>
                                <p className="text-sm text-gray-700 mb-2">
                                  과학 연구 결과를 인포그래픽으로 시각화하여 스토리와 피드에 게시하세요.
                                  전문가 협업 컨텐츠와 실제 사용자의 비포/애프터 결과물을 강조하세요.
                                </p>
                                <div className="flex gap-2">
                                  <Badge variant="secondary">인포그래픽</Badge>
                                  <Badge variant="secondary">전문가 협업</Badge>
                                  <Badge variant="secondary">비포/애프터</Badge>
                                </div>
                              </div>
                              
                              <div className="p-4 bg-gray-50 rounded-lg">
                                <div className="font-semibold mb-2">블로그</div>
                                <p className="text-sm text-gray-700 mb-2">
                                  상세한 성분 분석과 효능에 대한 심층 컨텐츠를 게시하세요.
                                  Q&A 형식의 컨텐츠로 소비자 불안 요소를 선제적으로 해소하세요.
                                </p>
                                <div className="flex gap-2">
                                  <Badge variant="secondary">심층 분석</Badge>
                                  <Badge variant="secondary">Q&A</Badge>
                                  <Badge variant="secondary">성분 설명</Badge>
                                </div>
                              </div>
                            </div>
                          </CardContent>
                          <CardFooter className="border-t pt-4">
                            <Button className="w-full">실행 전략 다운로드</Button>
                          </CardFooter>
                        </Card>
                        
                        <Card>
                          <CardHeader>
                            <CardTitle>실행 일정 제안</CardTitle>
                            <CardDescription>최적의 마케팅 일정 계획입니다.</CardDescription>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-3">
                              <div className="flex">
                                <div className="w-24 font-medium">1주차</div>
                                <div className="flex-1">브랜드 메시지 정립 및 과학적 검증 컨텐츠 준비</div>
                              </div>
                              <div className="flex">
                                <div className="w-24 font-medium">2주차</div>
                                <div className="flex-1">인스타그램 인포그래픽 시리즈 5회 게시</div>
                              </div>
                              <div className="flex">
                                <div className="w-24 font-medium">3주차</div>
                                <div className="flex-1">전문가 협업 컨텐츠 및 블로그 심층 분석 포스팅</div>
                              </div>
                              <div className="flex">
                                <div className="w-24 font-medium">4주차</div>
                                <div className="flex-1">고객 Q&A 세션 및 장기적 효과 관련 컨텐츠 강화</div>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </div>
                    </TabsContent>
                  </Tabs>
                </div>
              </div>
            )}
            
            {currentTab === 'mypage' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold">마이페이지</h2>
                    <div className="flex items-center gap-3">
                      <Badge variant="outline" className="px-3 py-1.5 bg-gray-50">
                        <CreditCard className="w-4 h-4 mr-1" /> 잔여 크레딧: 19
                      </Badge>
                      <Button>크레딧 충전</Button>
                    </div>
                  </div>
                  
                  <Tabs defaultValue="history">
                    <TabsList className="mb-6">
                      <TabsTrigger value="history">분석 이력</TabsTrigger>
                      <TabsTrigger value="favorites">즐겨찾기</TabsTrigger>
                      <TabsTrigger value="credits">크레딧 사용 내역</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="history">
                      <div className="mb-4 flex justify-between items-center">
                        <div className="flex items-center gap-2">
                          <Filter className="w-4 h-4 text-gray-500" />
                          <span className="text-sm text-gray-500">총 15개의 분석 이력</span>
                        </div>
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm">
                            <Download className="w-4 h-4 mr-1" /> 내보내기
                          </Button>
                        </div>
                      </div>
                      
                      <div className="space-y-3">
                        {historyData.map((item) => (
                          <Card key={item.id} className="border border-gray-200">
                            <div className="flex items-center p-4">
                              <div className="flex-1">
                                <div className="font-medium">{item.title}</div>
                                <div className="text-sm text-gray-500 flex items-center">
                                  <Clock className="w-3 h-3 mr-1" /> {item.date}
                                </div>
                              </div>
                              <div className="flex items-center gap-2">
                                <Badge variant="outline">{item.status}</Badge>
                                <Button variant="ghost" size="sm">
                                  <Star className="w-4 h-4" />
                                </Button>
                                <Button variant="outline" size="sm">보기</Button>
                              </div>
                            </div>
                          </Card>
                        ))}
                      </div>
                      
                      <div className="mt-4 flex justify-center">
                        <Button variant="outline">더 보기</Button>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="favorites">
                      <div className="text-center py-12">
                        <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                        <h3 className="text-lg font-medium text-gray-700 mb-2">즐겨찾기 항목이 없습니다</h3>
                        <p className="text-gray-500 mb-4">분석 결과를 즐겨찾기하여 빠르게 접근하세요.</p>
                        <Button onClick={() => setCurrentTab('analyze')}>
                          <Plus className="w-4 h-4 mr-1" /> 새 분석 만들기
                        </Button>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="credits">
                      <Card>
                        <CardHeader>
                          <CardTitle>크레딧 사용 내역</CardTitle>
                          <CardDescription>최근 30일 기준 사용 내역입니다.</CardDescription>
                        </CardHeader>
                        <CardContent>
                          <table className="w-full">
                            <thead>
                              <tr className="border-b border-gray-200">
                                <th className="text-left py-3 text-sm font-medium text-gray-500">내역</th>
                                <th className="text-right py-3 text-sm font-medium text-gray-500">변동</th>
                                <th className="text-right py-3 text-sm font-medium text-gray-500">일시</th>
                                <th className="text-right py-3 text-sm font-medium text-gray-500">잔액</th>
                              </tr>
                            </thead>
                            <tbody>
                              {creditHistory.map((item) => (
                                <tr key={item.id} className="border-b border-gray-100">
                                  <td className="py-3 text-sm">{item.type}</td>
                                  <td className={`py-3 text-sm text-right ${item.amount > 0 ? 'text-green-600' : 'text-gray-600'}`}>
                                    {item.amount > 0 ? `+${item.amount}` : item.amount}
                                  </td>
                                  <td className="py-3 text-sm text-right text-gray-500">{item.date}</td>
                                  <td className="py-3 text-sm text-right font-medium">{item.balance}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </CardContent>
                      </Card>
                    </TabsContent>
                  </Tabs>
                </div>
              </div>
            )}
            
            {currentTab === 'admin' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold">관리자 대시보드</h2>
                    <div className="flex gap-2">
                      <Button variant="outline">
                        <Download className="w-4 h-4 mr-1" /> 보고서 다운로드
                      </Button>
                      <Button variant="outline">
                        <Filter className="w-4 h-4 mr-1" /> 필터
                      </Button>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">전체 요청 수</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-3xl font-bold">1,249</div>
                        <div className="flex items-center text-sm text-green-600 mt-1">
                          <TrendingUp className="w-3 h-3 mr-1" /> 12.3% 증가
                        </div>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">누적 크레딧 사용량</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-3xl font-bold">3,827</div>
                        <div className="flex items-center text-sm text-green-600 mt-1">
                          <TrendingUp className="w-3 h-3 mr-1" /> 8.7% 증가
                        </div>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-500">활성 사용자</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-3xl font-bold">237</div>
                        <div className="flex items-center text-sm text-green-600 mt-1">
                          <TrendingUp className="w-3 h-3 mr-1" /> 5.2% 증가
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Card>
                      <CardHeader>
                        <CardTitle>최근 7일 요청 통계</CardTitle>
                        <CardDescription>일별 요청 수 추이</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="h-64">
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={weeklyData}>
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="name" />
                              <YAxis />
                              <Tooltip />
                              <Bar dataKey="value" fill="#6366F1" />
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader>
                        <CardTitle>채널별 분석 빈도</CardTitle>
                        <CardDescription>사용자 분석 채널 비율</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="h-64">
                          <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                              <Pie
                                data={channelData}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                outerRadius={80}
                                fill="#8884d8"
                                dataKey="value"
                                label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
                              >
                                {channelData.map((entry, index) => (
                                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                              </Pie>
                              <Tooltip />
                            </PieChart>
                          </ResponsiveContainer>
                        </div>
                      </CardContent>
                    </Card>
                    
                    <Card className="md:col-span-2">
                      <CardHeader>
                        <CardTitle>사용자 행동 데이터</CardTitle>
                        <CardDescription>분석부터 결과 활용까지의 사용자 행동 분석</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="h-64">
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={[
                              { name: '1월', 분석요청: 65, PDF다운로드: 28, 전략활용: 15 },
                              { name: '2월', 분석요청: 59, PDF다운로드: 32, 전략활용: 20 },
                              { name: '3월', 분석요청: 80, PDF다운로드: 43, 전략활용: 29 },
                              { name: '4월', 분석요청: 81, PDF다운로드: 45, 전략활용: 32 }
                            ]}>
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="name" />
                              <YAxis />
                              <Tooltip />
                              <Legend />
                              <Line type="monotone" dataKey="분석요청" stroke="#8884d8" />
                              <Line type="monotone" dataKey="PDF다운로드" stroke="#82ca9d" />
                              <Line type="monotone" dataKey="전략활용" stroke="#ffc658" />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </div>
            )}
          </>
        ) : (
          // 비로그인 상태의 랜딩 페이지
          <div className="max-w-4xl mx-auto py-20 text-center">
            <h1 className="text-4xl font-bold mb-6">AI 기반 마케팅 전략 자동화</h1>
            <p className="text-xl text-gray-600 mb-10">
              리뷰와 커뮤니티 데이터를 분석하여 최적의 마케팅 전략을 도출하는 Intrix
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
              <Card>
                <CardContent className="pt-6">
                  <FileText className="w-12 h-12 text-indigo-500 mx-auto mb-4" />
                  <h3 className="text-lg font-medium mb-2">감정과 무의식적 욕구 분석</h3>
                  <p className="text-gray-500 text-sm">다양한 리뷰와 커뮤니티 데이터에서 소비자의 진짜 욕구를 파악합니다.</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-6">
                  <Sparkles className="w-12 h-12 text-indigo-500 mx-auto mb-4" />
                  <h3 className="text-lg font-medium mb-2">AI 마케팅 전략 도출</h3>
                  <p className="text-gray-500 text-sm">데이터 기반으로 최적화된 마케팅 전략과 실행 방안을 제시합니다.</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-6">
                  <BarChart2 className="w-12 h-12 text-indigo-500 mx-auto mb-4" />
                  <h3 className="text-lg font-medium mb-2">상세한 분석 리포트</h3>
                  <p className="text-gray-500 text-sm">브랜딩 전략부터 실행 계획까지 상세한 리포트를 제공합니다.</p>
                </CardContent>
              </Card>
            </div>
            
            <div className="flex justify-center gap-4 mt-8">
              <Button className="px-8 py-6 text-lg">무료로 시작하기</Button>
              <Button variant="outline" className="px-8 py-6 text-lg">더 알아보기</Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default IntrixApp;