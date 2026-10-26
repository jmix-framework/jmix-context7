<Path>Add-ons > Charts > Series > Line series > Multiple value series</Path>

Charts that have value axis can have any number of them. Use the yAxisIndex property to indicate which value axis the series belongs to.

multiple-axes-line-series.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="dateValueVolumeDc"
                    class="io.jmix.uisamples.entity.DateValueVolume">
            <loader id="dateValueVolumeDl" readOnly="true"/>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:tooltip trigger="AXIS">
                <charts:axisPointer type="CROSS"/>
            </charts:tooltip>
            <charts:legend top="0"/>

            <charts:xAxes>
                <charts:xAxis/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis name="Value" position="LEFT" alignTicks="true">
                    <charts:axisLine show="true">
                        <charts:lineStyle color="#5470C6"/>
                    </charts:axisLine>
                </charts:yAxis>
                <charts:yAxis name="Volume" position="RIGHT" alignTicks="true">
                    <charts:axisLine show="true">
                        <charts:lineStyle color="#91CC75"/>
                    </charts:axisLine>
                </charts:yAxis>
            </charts:yAxes>

            <charts:dataSet>
                <charts:source dataContainer="dateValueVolumeDc"
                               categoryField="date" valueFields="value volume"/>
            </charts:dataSet>

            <charts:series>
                <charts:line name="Value" yAxisIndex="0">
                    <charts:itemStyle color="#5470C6"/>
                </charts:line>
                <charts:line name="Volume" yAxisIndex="1">
                    <charts:itemStyle color="#91CC75"/>
                </charts:line>
            </charts:series>
        </charts:chart>
    </layout>
</view>




MultipleAxesLineSeriesSample.java

package io.jmix.uisamples.view.flowui.charts.series.line.multipleaxes;

import io.jmix.core.LoadContext;
import io.jmix.core.Metadata;
import io.jmix.core.TimeSource;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.DateValueVolume;
import org.apache.commons.lang3.time.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Random;

@ViewController("multiple-axes-line-series")
@ViewDescriptor("multiple-axes-line-series.xml")
public class MultipleAxesLineSeriesSample extends StandardView {

    protected static final int DAYS_COUNT = 20;

    @Autowired
    protected Metadata metadata;
    @Autowired
    protected TimeSource timeSource;

    protected Random random = new Random();

    @Install(to = "dateValueVolumeDl", target = Target.DATA_LOADER)
    protected List<DateValueVolume> coordinateDlLoadDelegate(LoadContext<DateValueVolume> loadContext) {
        List<DateValueVolume> items = new ArrayList<>();
        Date startDate = DateUtils.addDays(timeSource.currentTimestamp(), -DAYS_COUNT);
        for (int i = 0; i < DAYS_COUNT; i++) {
            items.add(generateDateValueVolume(DateUtils.addDays(startDate, i), i));
        }

        return items;
    }

    protected DateValueVolume generateDateValueVolume(Date date, int i) {
        Long value = Math.round(random.nextDouble() * (20 + i)) + 20 + i;
        Long volume = Math.round(random.nextDouble() * (20 + i)) + i;

        return dateValueVolume(date, value, volume);
    }

    protected DateValueVolume dateValueVolume(Date date, Long value, Long volume) {
        DateValueVolume dateValueVolume = metadata.create(DateValueVolume.class);
        dateValueVolume.setDate(date.toInstant()
                .atZone(ZoneId.systemDefault())
                .toLocalDate());
        dateValueVolume.setValue(value);
        dateValueVolume.setVolume(volume);
        return dateValueVolume;
    }
}




DateValueVolume.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.JmixId;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import io.jmix.core.metamodel.annotation.JmixProperty;

import java.time.LocalDate;
import java.util.UUID;

@JmixEntity
public class DateValueVolume {

    @JmixGeneratedValue
    @JmixId
    private UUID id;

    @JmixProperty(mandatory = true)
    private LocalDate date;

    @JmixProperty(mandatory = true)
    private Long value;

    @JmixProperty(mandatory = true)
    private Long volume;

    public Long getVolume() {
        return volume;
    }

    public void setVolume(Long volume) {
        this.volume = volume;
    }

    public Long getValue() {
        return value;
    }

    public void setValue(Long value) {
        this.value = value;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    @InstanceName
    @DependsOnProperties({"date", "value", "volume"})
    public String getInstanceName() {
        return String.format("%s %s %s", date, value, volume);
    }

    @Override
    public String toString() {
        return "DateValueVolume{" +
                "date=" + date +
                ", value=" + value +
                ", volume=" + volume +
                '}';
    }
}


