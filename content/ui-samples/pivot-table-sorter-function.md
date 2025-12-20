<Path>Add-ons > PivotTable > PivotTable with sort</Path>

The sortersFunction element defines a JavaScript function that will be used for rows and columns captions sorting. In the example, we sort the data by the number of people who ate together, in descending order.

pivot-table-sorter-function.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:pvttbl="http://jmix.io/schema/pvttbl/ui">
    <data>
        <collection id="tipsDc"
                    class="io.jmix.uisamples.entity.TipInfo">
            <fetchPlan extends="_local"/>
            <loader id="tipsLoader">
                <query>
                    <![CDATA[select e from TipInfo e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <pvttbl:pivotTable id="pivotTable"
                           dataContainer="tipsDc"
                           height="100%"
                           width="100%">
            <pvttbl:properties>
                <pvttbl:property name="totalBill"/>
                <pvttbl:property name="tip"/>
                <pvttbl:property name="sex"/>
                <pvttbl:property name="smoker"/>
                <pvttbl:property name="day"/>
                <pvttbl:property name="time"/>
                <pvttbl:property name="size"/>
            </pvttbl:properties>
            <pvttbl:columns>
                <pvttbl:column value="size"/>
            </pvttbl:columns>
            <pvttbl:rows>
                <pvttbl:row value="sex"/>
            </pvttbl:rows>
        </pvttbl:pivotTable>
    </layout>
</view>



PivotTableSorterFunction.java

package io.jmix.uisamples.view.flowui.pivottable.sorterfunction;

import io.jmix.core.MessageTools;
import io.jmix.core.Metadata;
import io.jmix.core.metamodel.model.MetaClass;
import io.jmix.flowui.view.*;
import io.jmix.pivottableflowui.component.PivotTable;
import io.jmix.pivottableflowui.kit.component.model.JsFunction;
import io.jmix.uisamples.entity.TipInfo;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("pivot-table-sorter-function")
@ViewDescriptor("pivot-table-sorter-function.xml")
public class PivotTableSorterFunction extends StandardView {

    @ViewComponent
    protected PivotTable<TipInfo> pivotTable;

    @Autowired
    private Metadata metadata;
    @Autowired
    private MessageTools messageTools;

    @Subscribe
    public void onInit(final InitEvent event) {
        MetaClass metaClass = metadata.getClass(TipInfo.class);
        String sizeCaption = messageTools.getPropertyCaption(metaClass, "size");

        String sortersFunction = """
                    sortersFunction(property) {
                        if (property == "%s") {
                            return pivotTable.$jQuery.pivotUtilities.sortAs([6,5,4,3,2,1]);
                        }
                    }
                """.formatted(sizeCaption);

        pivotTable.setSortersFunction(new JsFunction(sortersFunction));
    }
}




TipInfo.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.springframework.lang.Nullable;

import java.math.BigDecimal;
import java.util.UUID;

@Table(name = "TIP_INFO")
@Entity
@JmixEntity
public class TipInfo {

    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    @Id
    private UUID id;

    @Column(name = "TOTAL_BILL", nullable = false, precision = 19, scale = 2)
    private BigDecimal totalBill;

    @Column(name = "TIP", nullable = false, precision = 19, scale = 2)
    private BigDecimal tip;

    @Column(name = "SMOKER", nullable = false)
    private Boolean smoker = false;

    @Column(name = "SIZE_", nullable = false)
    private Integer size;

    @Column(name = "SEX")
    private String sex;

    @Column(name = "DAY_")
    private String day;

    @Column(name = "TIME_")
    private String time;

    @Nullable
    public Time getTime() {
        return time == null ? null : Time.fromId(time);
    }

    public void setTime(@Nullable Time time) {
        this.time = time == null ? null : time.getId();
    }

    @Nullable
    public Day getDay() {
        return day == null ? null : Day.fromId(day);
    }

    public void setDay(@Nullable Day day) {
        this.day = day == null ? null : day.getId();
    }

    @Nullable
    public Sex getSex() {
        return sex == null ? null : Sex.fromId(sex);
    }

    public void setSex(@Nullable Sex sex) {
        this.sex = sex == null ? null : sex.getId();
    }

    public Integer getSize() {
        return size;
    }

    public void setSize(Integer size) {
        this.size = size;
    }

    public Boolean getSmoker() {
        return smoker;
    }

    public void setSmoker(Boolean smoker) {
        this.smoker = smoker;
    }

    public BigDecimal getTip() {
        return tip;
    }

    public void setTip(BigDecimal tip) {
        this.tip = tip;
    }

    public BigDecimal getTotalBill() {
        return totalBill;
    }

    public void setTotalBill(BigDecimal totalBill) {
        this.totalBill = totalBill;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}


