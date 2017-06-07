/* globals Logger */

export class CourseSock {  // eslint-disable-line import/prefer-default-export
  constructor() {
    const $toggleActionButton = $('.action-toggle-verification-sock');
    const $verificationSock = $('.verification-sock .verification-main-panel');
    const $upgradeToVerifiedButton = $('.verification-sock .action-upgrade-certificate');
    const onHomePage = window.location.href.indexOf('courseware') > -1;

    $toggleActionButton.on('click', () => {
      $toggleActionButton.toggleClass('active');
      $verificationSock.slideToggle(400);

      const isOpening = $toggleActionButton.hasClass('active');
      const logMessage = isOpening ? 'User opened the verification sock.' : 'User closed the verification sock.';
      Logger.log(
        logMessage,
        {
          from_course_home_page: onHomePage,
        },
      );
    });

    $upgradeToVerifiedButton.on('click', () => {
      Logger.log(
        'User clicked the upgrade button in the verification sock.',
        {
          from_course_home_page: onHomePage,
        },
      );
    });
  }
}
