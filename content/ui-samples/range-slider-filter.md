<Path>Components > RangeSlider > RangeSlider as a filter</Path>

A range slider is a natural filter control. This sample feeds both bounds of the selected range into the collection loader's query parameters and reloads the grid whenever the range changes.

Sliders use the `ON_CHANGE` value change mode by default, so the query runs once the user releases a handle rather than on every step of the drag. Read the bounds from the event value with `start()` and `end()`.


range-slider-filter.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_local">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e
                             where e.age >= :minAge and e.age <= :maxAge
                             order by e.age]]>
                </query>
            </loader>
        </collection>
    </data>
    <layout>
        <integerRangeSlider id="ageRangeSlider" label="Age" width="20em"
                            min="18" max="90" step="1"
                            startValue="25" endValue="50"
                            minMaxVisible="true"
                            accessibleNameStart="Minimum age" accessibleNameEnd="Maximum age"/>
        <dataGrid id="customersDataGrid" dataContainer="customersDc"
                  width="100%" minHeight="20em">
            <columns>
                <column property="name"/>
                <column property="lastName"/>
                <column property="age"/>
            </columns>
        </dataGrid>
    </layout>
</view>




RangeSliderFilterSample.java

package io.jmix.uisamples.view.flowui.components.rangeslider.filter;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.slider.IntegerRangeSlider;
import com.vaadin.flow.component.slider.IntegerRangeSliderValue;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;

@ViewController("range-slider-filter")
@ViewDescriptor("range-slider-filter.xml")
public class RangeSliderFilterSample extends StandardView {

    @ViewComponent
    protected IntegerRangeSlider ageRangeSlider;
    @ViewComponent
    protected CollectionLoader<Customer> customersDl;

    @Subscribe
    protected void onBeforeShow(BeforeShowEvent event) {
        loadCustomers(ageRangeSlider.getValue());
    }

    @Subscribe("ageRangeSlider")
    protected void onAgeRangeSliderValueChange(
            ComponentValueChangeEvent<IntegerRangeSlider, IntegerRangeSliderValue> event) {
        loadCustomers(event.getValue());
    }

    protected void loadCustomers(IntegerRangeSliderValue range) {
        customersDl.setParameter("minAge", range.start());
        customersDl.setParameter("maxAge", range.end());
        customersDl.load();
    }
}




Customer.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import org.jspecify.annotations.Nullable;

import java.util.UUID;

@Table(name = "CUSTOMER")
@Entity
@JmixEntity
public class Customer {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", length = 50, nullable = false)
    protected String name;

    @Column(name = "LAST_NAME", length = 100, nullable = false)
    protected String lastName;

    @Email
    @Column(name = "EMAIL", nullable = false)
    protected String email;

    @Column(name = "AGE")
    protected Integer age;

    @Column(name = "ACTIVE", nullable = false)
    protected Boolean active = false;

    @Column(name = "GRADE")
    protected Integer grade;

    public Boolean getActive() {
        return active;
    }

    public Customer() {
        this.id = UUID.randomUUID();
    }

    @InstanceName
    @DependsOnProperties({"name", "lastName"})
    public String getInstanceName() {
        return name + " " + lastName;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setGrade(@Nullable CustomerGrade grade) {
        this.grade = grade == null ? null : grade.getId();
    }

    @Nullable
    public CustomerGrade getGrade() {
        return grade == null ? null : CustomerGrade.fromId(grade);
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Boolean isActive() {
        return active;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getAge() {
        return age;
    }
}


