import emailjs from 'emailjs-com';

const COUNTER_KEY = 'questionnaire_count';
const DEPLOY_VERSION = '2024-12-09'; // 每次部署时更新这个版本号

// 从邮件主题解析当前计数
const parseCountFromSubject = (subject) => {
  const match = subject.match(/当前计数:(\d+)/);
  return match ? parseInt(match[1]) : 0;
};

// 重置计数
const resetCount = async () => {
  try {
    await emailjs.send(
      'service_w28zafs',
      'template_cq4vqhy',
      {
        to_email: 'zxx729149195@163.com',
        subject: `当前计数:0`,
        message: `问卷计数已重置 (部署版本: ${DEPLOY_VERSION})`
      },
      'zEOYsF4TFcaSSPSsZ'
    );
  } catch (error) {
    console.error('Error resetting count:', error);
  }
};

// 获取当前计数
export const getSubmissionCount = async () => {
  try {
    const response = await emailjs.send(
      'service_w28zafs',
      'template_cq4vqhy',
      {
        to_email: 'zxx729149195@163.com',
        subject: '查询计数',
        message: '查询当前问卷数量'
      },
      'zEOYsF4TFcaSSPSsZ'
    );

    const count = parseCountFromSubject(response.text);
    return count;
  } catch (error) {
    console.error('Error fetching count:', error);
    return 0;
  }
};

// 增加计数
export const incrementCount = async () => {
  try {
    const currentCount = await getSubmissionCount();
    const newCount = currentCount + 1;
    
    await emailjs.send(
      'service_w28zafs',
      'template_cq4vqhy',
      {
        to_email: 'zxx729149195@163.com',
        subject: `当前计数:${newCount}`,
        message: `收到新的问卷提交,当前总数: ${newCount} (部署版本: ${DEPLOY_VERSION})`
      },
      'zEOYsF4TFcaSSPSsZ'
    );
    
    return newCount;
  } catch (error) {
    console.error('Error incrementing count:', error);
    return 0;
  }
};

// 导出重置函数
export const resetSubmissionCount = resetCount; 