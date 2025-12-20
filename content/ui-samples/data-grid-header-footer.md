<Path>Components > DataGrid > Header and footer</Path>

DataGrid supports prependHeaderRow(), appendHeaderRow() and prependFooterRow(), appendFooterRow() methods. These cells may be merged for multiple columns.

data-grid-header-footer.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="countryGrowthDc"
                    class="io.jmix.uisamples.entity.CountryGrowth"
                    fetchPlan="_local">
            <loader id="countryGrowthDl">
                <query>
                    <![CDATA[select e from CountryGrowth e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <dataGrid id="dataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="countryGrowthDc"
                  themeNames="column-borders row-stripes">
            <columns>
                <column property="country"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridHeaderFooterSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.headerfooter;

import com.vaadin.flow.component.Html;
import com.vaadin.flow.component.Text;
import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.grid.FooterRow;
import com.vaadin.flow.component.grid.HeaderRow;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import io.jmix.core.MessageTools;
import io.jmix.core.Metadata;
import io.jmix.core.metamodel.model.MetaClass;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.CountryGrowth;
import org.springframework.beans.factory.annotation.Autowired;

import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Collection;

@ViewController("data-grid-header-footer")
@ViewDescriptor("data-grid-header-footer.xml")
public class DataGridHeaderFooterSample extends StandardView {

    @ViewComponent
    protected DataGrid<CountryGrowth> dataGrid;

    @Autowired
    protected MessageTools messageTools;
    @Autowired
    protected Metadata metadata;

    protected DecimalFormat percentFormat;

    @Subscribe
    protected void onInit(InitEvent event) {
        initPercentFormat();
        initColumns();
        initHeader();
    }

    @Subscribe
    protected void onBeforeShow(BeforeShowEvent event) {
        //because data is loaded
        initFooter();
    }

    protected void initPercentFormat() {
        percentFormat = (DecimalFormat) NumberFormat.getPercentInstance(UI.getCurrent().getLocale());
        percentFormat.setMultiplier(1);
        percentFormat.setMaximumFractionDigits(2);
    }

    protected void initColumns() {
        MetaClass metaClass = metadata.getClass(CountryGrowth.class);
        dataGrid.addComponentColumn(countryGrowth -> new Text(percentFormat.format(countryGrowth.getPrevYear())))
                .setHeader(messageTools.getPropertyCaption(metaClass, "prevYear"))
                .setKey("prevYear");
        dataGrid.addComponentColumn(countryGrowth -> new Text(percentFormat.format(countryGrowth.getCurrYear())))
                .setHeader(messageTools.getPropertyCaption(metaClass, "currYear"))
                .setKey("currYear");
    }

    protected void initHeader() {
        HeaderRow headerRow = dataGrid.prependHeaderRow();
        HeaderRow.HeaderCell headerCell = headerRow.join(
                dataGrid.getColumnByKey("prevYear"),
                dataGrid.getColumnByKey("currYear")
        );

        Span gdpGrowth = new Span("GDP growth");
        HorizontalLayout layout = new HorizontalLayout(gdpGrowth);

        layout.setJustifyContentMode(FlexComponent.JustifyContentMode.CENTER);
        headerCell.setComponent(layout);
    }

    protected void initFooter() {
        FooterRow footerRow = dataGrid.appendFooterRow();

        FooterRow.FooterCell countryCell = footerRow.getCell(dataGrid.getColumnByKey("country"));
        Html html = new Html("<strong> Average: </strong>");
        countryCell.setComponent(html);

        footerRow.getCell(dataGrid.getColumnByKey("prevYear"))
                .setText(percentFormat.format(getAverage("prevYear")));
        footerRow.getCell(dataGrid.getColumnByKey("currYear"))
                .setText(percentFormat.format(getAverage("currYear")));

    }

    protected double getAverage(String propertyId) {
        double average = 0.0;

        Collection<CountryGrowth> items = dataGrid.getGenericDataView().getItems().toList();
        for (CountryGrowth countryGrowth : items) {
            Double value = propertyId.equals("prevYear")
                    ? countryGrowth.getPrevYear()
                    : countryGrowth.getCurrYear();

            average += value != null ? value : 0.0;
        }
        return average / items.size();
    }
}




CountryGrowth.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@Table(name = "COUNTRY_GROWTH")
@Entity
@JmixEntity
public class CountryGrowth {

    @Id
    @Column(name = "ID")
    @JmixGeneratedValue
    protected UUID id;

    @InstanceName
    @Column(name = "COUNTRY", nullable = false)
    protected String country;

    @Column(name = "FLAG")
    private String flag;

    @Column(name = "PREV_YEAR", nullable = false)
    protected Double prevYear;

    @Column(name = "CURR_YEAR", nullable = false)
    protected Double currYear;

    public CountryGrowth() {
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getFlag() {
        return flag;
    }

    public void setFlag(String flag) {
        this.flag = flag;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public Double getPrevYear() {
        return prevYear;
    }

    public void setPrevYear(Double prevYear) {
        this.prevYear = prevYear;
    }

    public Double getCurrYear() {
        return currYear;
    }

    public void setCurrYear(Double currYear) {
        this.currYear = currYear;
    }
}


