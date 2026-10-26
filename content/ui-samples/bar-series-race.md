<Path>Add-ons > Charts > Series > Bar series > Bar Race</Path>

A bar race is a bar chart that reorders its bars as the values change. Set `realtimeSort` on the `bar` series to sort the bars by value on every update.

Click **Start** to run the race. The timer increases the sales every two seconds, and the controller passes the changed items to `updateItem()` of `ListChartItems`. The chart updates the data set without rebuilding. **Stop** pauses the timer.

`inverse` on the category axis puts the largest bar at the top. `animationDurationUpdate` and `animationEasingUpdate` of the chart make the bars grow smoothly for the whole interval between updates. The shorter `animationDurationUpdate` of the axis moves the bars to their new places faster.


bar-series-race.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <facets>
        <timer id="timer"
               delay="2000"
               autostart="false"
               repeating="true"/>
    </facets>
    <layout>
        <hbox padding="false">
            <button id="startStopRace"/>
        </hbox>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em"
                      animationDuration="0"
                      animationDurationUpdate="2000"
                      animationEasing="linear"
                      animationEasingUpdate="linear">
            <charts:title text="Sales" subtext="By products" left="0" top="0"/>

            <charts:xAxes>
                <charts:xAxis type="VALUE" max="dataMax"/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis type="CATEGORY" inverse="true"
                              animationDuration="300" animationDurationUpdate="300"/>
            </charts:yAxes>

            <charts:series>
                <charts:bar name="Sales" realtimeSort="true">
                    <charts:label show="true" position="RIGHT"/>
                </charts:bar>
            </charts:series>
        </charts:chart>
    </layout>
</view>




BarSeriesRaceSample.java

package io.jmix.uisamples.view.flowui.charts.series.bar.race;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.button.ButtonVariant;
import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.facet.Timer;
import io.jmix.flowui.icon.Icons;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.kit.icon.JmixFontIcon;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Map;
import java.util.Random;
import java.util.stream.Stream;

@ViewController("bar-series-race")
@ViewDescriptor("bar-series-race.xml")
public class BarSeriesRaceSample extends StandardView {

    @ViewComponent
    private Chart chart;
    @ViewComponent
    private Timer timer;
    @ViewComponent
    private JmixButton startStopRace;

    @Autowired
    private Icons icons;

    private final ListChartItems<MapDataItem> items = new ListChartItems<>();
    private final Random random = new Random();
    private boolean raceStarted;

    @Subscribe
    protected void onInit(InitEvent event) {
        Stream.of("Laptops", "Phones", "Tablets", "Monitors", "Printers", "Cameras", "Headphones", "Speakers")
                .map(this::toMapDataItem)
                .forEach(items::addItem);

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(items)
                                        .withCategoryField("product")
                                        .withValueField("sales")
                        )
        );

        prepareButtonToStart();
    }

    @Subscribe(id = "startStopRace", subject = "clickListener")
    public void onStartStopRaceClick(final ClickEvent<JmixButton> event) {
        if (raceStarted) {
            timer.stop();
            prepareButtonToStart();
        } else {
            timer.start();
            prepareButtonToStop();
        }

        raceStarted = !raceStarted;
    }

    @Subscribe("timer")
    public void onTimerTick(Timer.TimerActionEvent event) {
        for (MapDataItem item : items.getItems()) {
            int sales = (int) item.getValue("sales") + random.nextInt(0, 500);
            items.updateItem(item.add("sales", sales));
        }
    }

    private MapDataItem toMapDataItem(String product) {
        return new MapDataItem(Map.of("product", product,
                "sales", random.nextInt(100, 1000)));
    }

    private void prepareButtonToStart() {
        startStopRace.setText("Start");
        startStopRace.setIcon(icons.get(JmixFontIcon.PLAY));
        startStopRace.addThemeVariants(ButtonVariant.PRIMARY);
        startStopRace.removeThemeVariants(ButtonVariant.ERROR);
    }

    private void prepareButtonToStop() {
        startStopRace.setText("Stop");
        startStopRace.setIcon(icons.get(JmixFontIcon.PAUSE));
        startStopRace.addThemeVariants(ButtonVariant.ERROR);
    }
}


