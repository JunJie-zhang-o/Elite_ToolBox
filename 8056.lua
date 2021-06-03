--将16进制串转换为字符串
--如\x12\x34\xAB\xCD”转为“1234ABCD
function hex2str(hex)
    --判断输入类型
    if (type(hex)~="string") then
        return nil,"hex2str invalid input type"
    end
    --拼接字符串
    local index=1
    local ret=""
    for index=1,hex:len() do
        ret=ret..string.format("%02X",hex:sub(index):byte())
    end
    return ret
end

-- 字符串转16进制
-- 如1234ABCD转为\x12\x34\xAB\xCD
function str2hex(str)
    --判断输入类型
    if (type(str)~="string") then
        return nil,"str2hex invalid input type"
    end
    --滤掉分隔符
    str=str:gsub("[%s%p]",""):upper()
    --检查内容是否合法
    if(str:find("[^0-9A-Fa-f]")~=nil) then
        return nil,"str2hex invalid input content"
    end
    --检查字符串长度
    if(str:len()%2~=0) then
        return nil,"str2hex invalid input lenth"
    end
    --拼接字符串
    local index=1
    local ret=""
    for index=1,str:len(),2 do
        ret=ret..string.char(tonumber(str:sub(index,index+1),16))
    end
    return ret
end

function hex2float( hexString )
	if hexString == nil then
		return 0
	end
	local t = type( hexString )
	if t == "string" then
		hexString = tonumber(hexString , 16)
	end
 
	local hexNums = hexString
    print(hexNums)
	local sign = math.modf(hexNums/(2^31))
    print(sign)
	local exponent = hexNums % (2^31)
	exponent = math.modf(exponent/(2^23)) -127
 
	local mantissa = hexNums % (2^23)
 
	for i=1,23 do
		mantissa = mantissa / 2
	end
	mantissa = 1+mantissa
	local result = (-1)^sign * mantissa * 2^exponent
	return result
end


function hex2double( hexString )
	if hexString == nil then
		return 0
	end
	local t = type( hexString )
	if t == "string" then
		hexString = tonumber(hexString , 16)
        print(hexString)
	end
 
	local hexNums = hexString
    print(hexNums)
	local sign = math.modf(hexNums/(2^63))
    print(sign)
	local exponent = hexNums % (2^63)
	exponent = math.modf(exponent/(2^52)) -1023
 
	local mantissa = hexNums % (2^52)
 
	for i=1,52 do
		mantissa = mantissa / 2
	end
	mantissa = 1+mantissa
	local result = (-1)^sign * mantissa * 2^exponent
	return result
end



function convert(hex)
	-- body
	-- hex = string.reverse(hex)
    print(hex)
	local hex_str = hex2str(hex)
    print(hex_str)
	-- return hex2double(hex_str)
	return hex2float(hex)
end


function anal(buff)


	F1 = convert(buff)

    print(F1)

end




-- local a=353.05157335486115
-- local b=string.pack(">d",a)
-- print(#b)

local c="@v\x10\xd3>\x95\x07\x94"
local c='@N\xd32\xcf\xa6\xa7\xa4'
-- local c='@x^\xbb\x94m=Z'
-- local c='\xc0\x08\xe0\x8e=f\xebM'
local c='\xbf\x991\x97Z\x91+d'
-- local c="C11C75B0"
local c="40F05CAE"
print(c)
print(type(c))
-- print(string.unpack(">d",c))

-- local d="\x10\xd3\x95\x07\x94"
-- -- print(d)
-- print(hex2str(d))
anal(c)


-- double为8个字节,64位，最高位为符号位，指数长度为11位，尾数长度为52位，偏差为1023
-- float为4个字节,32位，最高位为符号位，指数长度为8位，尾数长度为23位，偏差为127

