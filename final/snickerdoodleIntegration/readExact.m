function data = readExact(client, nBytes)
    data = uint8([]);
    while numel(data) < nBytes
        chunk = read(client, nBytes - numel(data), "uint8");
        if isempty(chunk)
            error("Socket read returned empty before receiving all bytes.");
        end
        data = [data; chunk(:)]; %#ok<AGROW>
    end
end