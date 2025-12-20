<Path>Facets > Timer</Path>

Timer is a facet (non-visual component) designed to run UI code at specified time intervals. The timer action is initiated from the browser as a user request and its handler can update UI components. The timer stops working when the view it was created for is closed. Timers are defined using the timer element. It has the following attributes: delay - defines timer interval in milliseconds; autostart - if set to true, the timer starts immediately after the view is opened. By default, the value is false, witch means that the timer will start only when its start() method is invoked; repeating - turns on repeated execution of the timer. If the attribute is set to true, the timer runs in cycles at equals intervals defined in the delay attribute. Otherwise, the timer runs only once - delay milliseconds after the timer start. To execute code on timer, subscribe to its TimerActionEvent in the view controller. See also the example of how to use timer to delay a costly data loading operation until the user has made the final selection of conditions.

timer-facet.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <facets>
        <timer id="timer"
               delay="3000"
               autostart="false"
               repeating="true"/>
    </facets>
    <layout classNames="flex-row flex-wrap" alignItems="CENTER">
        <button id="timerStartBtn" text="Start" icon="PLAY" themeNames="primary"/>
        <button id="timerStopBtn" text="Stop" icon="PAUSE" themeNames="primary error" enabled="false"/>
        <span id="timerIndicator" text="Timer is ready to start" themeNames="badge contrast pill"/>
    </layout>
</view>




TimerFacetSample.java

package io.jmix.uisamples.view.flowui.facets.timer;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.facet.Timer;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("timer-facet")
@ViewDescriptor("timer-facet.xml")
public class TimerFacetSample extends StandardView {

    @ViewComponent
    protected Timer timer;
    @ViewComponent
    protected Span timerIndicator;
    @ViewComponent
    protected JmixButton timerStartBtn;
    @ViewComponent
    protected JmixButton timerStopBtn;

    @Autowired
    protected Notifications notifications;

    protected int seconds = 0;
    protected int ticks = 0;

    @Subscribe("timerStartBtn")
    protected void onStartTimerClick(ClickEvent<JmixButton> event) {
        timer.start();

        timerIndicator.setText("Timer started");
        timerIndicator.getElement().getThemeList().clear();
        timerIndicator.getElement().getThemeList().add("badge pill success");

        notifications.create("Timer started")
                .withPosition(Notification.Position.BOTTOM_END)
                .withThemeVariant(NotificationVariant.LUMO_SUCCESS)
                .show();

        timerStartBtn.setEnabled(false);
        timerStopBtn.setEnabled(true);
    }

    @Subscribe("timerStopBtn")
    protected void onStopTimerClick(ClickEvent<JmixButton> event) {
        timer.stop();
        seconds = 0;

        timerIndicator.setText("Timer stopped");
        timerIndicator.getElement().getThemeList().clear();
        timerIndicator.getElement().getThemeList().add("badge pill error");

        timerStartBtn.setEnabled(true);
        timerStopBtn.setEnabled(false);
    }

    @Subscribe("timer")
    protected void onTimerTick(Timer.TimerActionEvent event) {
        ++ticks;
        seconds += event.getSource().getDelay() / 1000;

        notifications.create("Timer tick", seconds + " seconds passed")
                .withDuration(2750)
                .show();
    }

    @Subscribe("timer")
    protected void onTimerStop(Timer.TimerStopEvent event) {
        notifications.create("Timer stopped", "Number of ticks: " + ticks)
                .withThemeVariant(NotificationVariant.LUMO_PRIMARY)
                .withDuration(5000)
                .show();
        ticks = 0;
    }
}


