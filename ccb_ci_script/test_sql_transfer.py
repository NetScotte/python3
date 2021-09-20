# -*- coding=utf-8 -*-
import pytest
from sql_transfer import escape_semicolon


def test_escape_semicolon_with_not_found_file(tmpdir):
    """测试文件不存在的情况"""
    filename = tmpdir.join('test.sql')
    with pytest.raises(FileNotFoundError) as excinfo:
        escape_semicolon(filename)
    assert f'{filename}不存在' in str(excinfo.value)


def test_escape_semicolon_with_success(tmpdir):
    filename = tmpdir.join('test.sql')
    s = r"""
insert into channel.BDF_ENUMS(id_,name_,category_id_,code,desc_,DATALEVEL,id_forkey) values('ExecSql1','ExecSql1','lis_lcpol','ExecSql1','declare
  cursor cur_data is
    select t.sysevttraceid,
           t.batchno
      from imp_lis_lcpol t;
  v_cur_data_type cur_data%rowtype;
  v_count         number := 0;
  v_sqlerrm       varchar2(300);
  v_number        number;
begin
  open cur_data;
  loop
    fetch cur_data
      into v_cur_data_type;
    exit when cur_data%notfound;
    v_count := v_count + 1;
    begin
      select count(1)
        into v_number
        from tbl_lis_lcpol t
       where t.polno = v_cur_data_type.polno;
      if v_number >= 0 then
        update tbl_lis_lcpol t
           set sysevttraceid = v_cur_data_type.sysevttraceid,
               contno        = v_cur_data_type.contno,
         where t.polno = v_cur_data_type.polno;
      else
        ',1,channel.SEQ_BDF_ENUMS.nextval);
"""
    filename.write(s)
    result = escape_semicolon(filename)
    assert result == r"""
insert into channel.BDF_ENUMS(id_,name_,category_id_,code,desc_,DATALEVEL,id_forkey) values('ExecSql1','ExecSql1','lis_lcpol','ExecSql1','declare
  cursor cur_data is
    select t.sysevttraceid,
           t.batchno
      from imp_lis_lcpol t'||';'||'
  v_cur_data_type cur_data%rowtype'||';'||'
  v_count         number := 0'||';'||'
  v_sqlerrm       varchar2(300)'||';'||'
  v_number        number'||';'||'
begin
  open cur_data'||';'||'
  loop
    fetch cur_data
      into v_cur_data_type'||';'||'
    exit when cur_data%notfound'||';'||'
    v_count := v_count + 1'||';'||'
    begin
      select count(1)
        into v_number
        from tbl_lis_lcpol t
       where t.polno = v_cur_data_type.polno'||';'||'
      if v_number >= 0 then
        update tbl_lis_lcpol t
           set sysevttraceid = v_cur_data_type.sysevttraceid,
               contno        = v_cur_data_type.contno,
         where t.polno = v_cur_data_type.polno'||';'||'
      else
        ',1,channel.SEQ_BDF_ENUMS.nextval);
"""
