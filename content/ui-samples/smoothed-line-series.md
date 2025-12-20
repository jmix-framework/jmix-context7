<Path>Add-ons > Charts > Series > Line series > Smoothed Line series</Path>

LineSeries can be smoothed by setting smooth property to a value in the range [0, 1] in the series element.

smoothed-line-series.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="dateValueDc"
                    class="io.jmix.uisamples.entity.DateValue">
            <fetchPlan extends="_local"/>
            <loader id="dateValueDl" readOnly="true">
                <query>
                    <![CDATA[select e from DateValue e order by e.date]]>
                </query>
            </loader>
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

            <charts:xAxes>
                <charts:xAxis type="TIME">
                    <charts:minorSplitLine show="true"/>
                </charts:xAxis>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis>
                    <charts:minorSplitLine show="true"/>
                </charts:yAxis>
            </charts:yAxes>

            <charts:dataSet>
                <charts:source dataContainer="dateValueDc"
                               categoryField="date" valueFields="value"/>
            </charts:dataSet>

            <charts:series>
                <charts:line id="line" name="Value"
                             smooth="0.4"
                             symbolSize="7"
                             showAllSymbol="false" symbol="circle">
                    <charts:itemStyle color="RED"/>
                </charts:line>
            </charts:series>
        </charts:chart>
    </layout>
</view>




SmoothedLineSample.java

package io.jmix.uisamples.view.flowui.charts.series.line.smoothed;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("smoothed-line-series")
@ViewDescriptor("smoothed-line-series.xml")
public class SmoothedLineSample extends StandardView {
}




DateValue.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;
import java.util.UUID;

@JmixEntity
@Table(name = "DATE_VALUE")
@Entity
public class DateValue {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @NotNull
    @Column(name = "DATE_", nullable = false)
    private LocalDate date;

    @NotNull
    @Column(name = "VALUE_", nullable = false)
    private Integer value;

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public LocalDate getDate() {
        return date;
    }

    public Integer getValue() {
        return value;
    }

    public void setValue(Integer value) {
        this.value = value;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    @InstanceName
    @DependsOnProperties({"date", "value"})
    public String getInstanceName() {
        return String.format("%s %s", date, value);
    }
}


